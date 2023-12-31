import argparse
import json
import logging

import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, PreTrainedModel, get_scheduler

from genbench import load_task


##########################################################
# Data Loadig Utils
##########################################################
class Dataset(torch.utils.data.Dataset):
    def __init__(self, features):
        self.features = features

    def __getitem__(self, index):
        return self.features[index]

    def __len__(self):
        return len(self.features)


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""

    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


def _convert_examples_to_features(
    comments,
    codes,
    labels,
    max_seq_length,
    tokenizer,
    cls_token="[CLS]",
    sep_token="[SEP]",
    pad_token=0,
    eos_token="</s>",
    sequence_a_segment_id=0,
    sequence_b_segment_id=1,
    cls_token_segment_id=1,
    pad_token_segment_id=0,
    mask_padding_with_zero=True,
):
    features = []
    for ex_index, (comment, code, label) in enumerate(zip(comments, codes, labels)):
        # As was done in CodeBERT
        tokens_comment = tokenizer.tokenize(comment)[:50]
        tokens_code = tokenizer.tokenize(code)

        # update max_seq_length to account for [CLS], [SEP], [SEP] tokens (-3)
        n_special_tokens = 3
        if cls_token is None:
            n_special_tokens -= 1
        s_max_seq_length = max_seq_length - n_special_tokens
        _truncate_seq_pair(tokens_comment, tokens_code, s_max_seq_length)

        # change sep for eos if no sep_token
        if sep_token is None:
            sep_token = eos_token

        # [SEP] inbetween and at the end
        tokens = tokens_comment + [sep_token] + tokens_code + [sep_token]
        # CLS at the beginning
        if cls_token is not None:
            tokens = [cls_token] + tokens

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # 1 for tokens, 0 for padding
        input_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        # padding with 0 up to max_seq_length
        padding_length = max_seq_length - len(input_ids)
        input_ids = input_ids + ([pad_token] * padding_length)
        input_mask = input_mask + ([0 if mask_padding_with_zero else 1] * padding_length)

        # check
        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length

        # convert to tensors
        input_ids = torch.tensor(input_ids, dtype=torch.long)
        input_mask = torch.tensor(input_mask, dtype=torch.long)
        label = torch.tensor(label, dtype=torch.long)

        features.append({"input_ids": input_ids, "attention_mask": input_mask, "labels": label})
    return features


def load_data(tokenizer, batch_size, seq_len, train_file, is_train):
    # create dataset
    comments = []
    codes = []
    labels = []
    skipped = 0

    is_sep_token_set = tokenizer.sep_token is not None
    is_cls_token_set = tokenizer.cls_token is not None
    is_pad_token_set = tokenizer.pad_token is not None
    is_eos_token_set = tokenizer.eos_token is not None

    for split, dataset in train_file.items():
        if is_train and split == "test":
            continue
        if not is_train and split == "train":
            continue
        for sample in dataset:
            try:
                input = sample["input"]
                # split at [CODESPLIT] token
                input = input.split("[CODESPLIT]")
                if len(input) != 2:
                    # skip cases with more than one [SEP] token
                    logging.warning(f"Input contains more than one [CODESPLIT] token: {input}")
                    skipped += 1
                    continue
                # skip every sample that contains special tokens
                if is_sep_token_set and (tokenizer.sep_token in input[0] or tokenizer.sep_token in input[1]):
                    logging.warning(f"Input contains special tokens: {input}")
                    skipped += 1
                    continue
                if is_cls_token_set and (tokenizer.cls_token in input[0] or tokenizer.cls_token in input[1]):
                    logging.warning(f"Input contains special tokens: {input}")
                    skipped += 1
                    continue
                if is_pad_token_set and (tokenizer.pad_token in input[0] or tokenizer.pad_token in input[1]):
                    logging.warning(f"Input contains special tokens: {input}")
                    skipped += 1
                    continue
                if is_eos_token_set and (tokenizer.eos_token in input[0] or tokenizer.eos_token in input[1]):
                    logging.warning(f"Input contains special tokens: {input}")
                    skipped += 1
                    continue
                comments.append(input[0])
                codes.append(input[1])
                labels.append(sample["target"])
            except json.JSONDecodeError as e:
                print(f"Error: JSON decoding failed - {e}")
                continue
    logging.info(f"Skipped {skipped} samples due to special tokens")
    # tokenize
    features = _convert_examples_to_features(
        comments,
        codes,
        labels,
        max_seq_length=seq_len,
        tokenizer=tokenizer,
        cls_token=tokenizer.cls_token,
        sep_token=tokenizer.sep_token,
        cls_token_segment_id=tokenizer.cls_token_id,
        pad_token_segment_id=tokenizer.pad_token_id,
        eos_token=tokenizer.eos_token,
    )

    # Convert to Dataset
    features = Dataset(features)

    return DataLoader(features, batch_size=batch_size, shuffle=True)


##############################################################
# Fine-tune Model
##############################################################


def train(model: PreTrainedModel, dataloader: DataLoader, args: argparse.Namespace):
    """
    Fine-tune the model.
    :param model: the pretrained model to be fine-tuned
    :param dataloader: an iterable data loader
    :param args: training arguments (and also some other arguments)
    :return: the fine-tuned model
    """

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = "cpu"
    model.to(device)
    model.train()

    num_training_steps = args.epochs * len(dataloader)
    progress_bar = tqdm(range(num_training_steps))

    optimizer = AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
    lr_scheduler = get_scheduler(
        name="linear",
        optimizer=optimizer,
        num_warmup_steps=args.num_warmup_steps,
        num_training_steps=num_training_steps,
    )

    for epoch in range(args.epochs):
        for batch in dataloader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()

            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()
            progress_bar.update(1)


###########################################################
# Evaluate Model
###########################################################


def clf(model, dataloader, args):
    """Predict on test set."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    predictions = []
    labels = []
    logging.info("Evaluating...")
    for batch in tqdm(dataloader):
        batch = {k: v.to(device) for k, v in batch.items()}
        with torch.no_grad():
            outputs = model(**batch)
            predictions.extend(outputs.logits.argmax(-1).cpu().numpy().tolist())
            labels.extend(batch["labels"].cpu().numpy().tolist())

    metrics = {}
    # calc metrics

    # calc accuracy
    accuracy = accuracy_score(labels, predictions)
    metrics["accuracy"] = accuracy

    # calc precision
    precision = precision_score(labels, predictions)
    metrics["precision"] = precision

    # calc recall
    recall = recall_score(labels, predictions)
    metrics["recall"] = recall

    # calc f1
    f1 = f1_score(labels, predictions)
    metrics["f1"] = f1

    return metrics


##############################################################
#  Run example
##############################################################


def main():
    """Main function."""
    # args
    parser = argparse.ArgumentParser()
    # parser.add_argument('--dataset', type=str, default='./codesearchnet_adv')
    parser.add_argument("--model", default="roberta-base")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--learning_rate", type=float, default=2e-5)
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--num_warmup_steps", type=int, default=0)
    parser.add_argument("--output_dir", type=str, default="models")
    parser.add_argument("--seq_len", type=int, default=512, help="maximum sequence length")
    # parser.add_argument("--distractors", type=int, default=99, help="number of distractors per true pair")
    parser.add_argument("--log_level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")

    args = parser.parse_args()

    TRAIN_FILE = load_task("nl_codesearch_clf:codesearchnet_adv").get_dataset_raw()

    # logging
    logging.basicConfig(level=args.log_level)

    # load tokenizer
    logging.info("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(args.model)

    # load data
    logging.info("Loading data...")
    dataloader = load_data(tokenizer, args.batch_size, args.seq_len, TRAIN_FILE, True)

    model = AutoModelForSequenceClassification.from_pretrained(args.model)

    # train
    logging.info("Training...")
    # train(model, dataloader, args)

    # save model
    logging.info("Saving model...")
    model.save_pretrained(f"{args.output_dir}/{args.model}")
    # also soave tokenizer
    tokenizer.save_pretrained(f"{args.output_dir}/{args.model}")

    TEST_FILES = [
        ["codesearchnetadv", load_task("nl_codesearch_clf:codesearchnet_adv").get_dataset_raw()],
        ["codesearchnet_ruby", load_task("nl_codesearch_clf:codesearchnet_ruby").get_dataset_raw()],
        ["codesearchnet_go", load_task("nl_codesearch_clf:codesearchnet_go").get_dataset_raw()],
        ["codesearchnet_java", load_task("nl_codesearch_clf:codesearchnet_java").get_dataset_raw()],
        ["codesearchnet_javascript", load_task("nl_codesearch_clf:codesearchnet_javascript").get_dataset_raw()],
        ["codesearchnet_php", load_task("nl_codesearch_clf:codesearchnet_php").get_dataset_raw()],
        ["cosqa", load_task("nl_codesearch_clf:cosqa").get_dataset_raw()],
        ["statcodesearch", load_task("nl_codesearch_clf:statcodesearch").get_dataset_raw()],
    ]

    results = {}
    for file in TEST_FILES:
        logging.info(f"Evaluating on {file[0]}...")
        dataloader = load_data(tokenizer, args.batch_size, args.seq_len, file[1], False)
        metrics = clf(model, dataloader, args)
        results[file[0]] = metrics
        logging.info(f"Test results for {file[0]}: {metrics}")

    logging.info(f"Test results: {results}")


if __name__ == "__main__":
    main()
