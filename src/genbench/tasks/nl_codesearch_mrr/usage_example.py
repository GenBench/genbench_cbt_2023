import argparse
import json
import logging
import random

import numpy as np
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, PreTrainedModel, get_scheduler


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


def load_data(tokenizer, batch_size, seq_len, train_file):
    # create dataset
    comments = []
    codes = []
    labels = []
    skipped = 0

    is_sep_token_set = tokenizer.sep_token is not None
    is_cls_token_set = tokenizer.cls_token is not None
    is_pad_token_set = tokenizer.pad_token is not None
    is_eos_token_set = tokenizer.eos_token is not None

    with open(train_file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                item = json.loads(line.strip())
                input = item["input"]
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
                labels.append(item["target"])
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


def load_data_for_mrr(tokenizer, file):
    # create dataset
    comments = []
    codes = []
    labels = []
    skipped = 0

    is_sep_token_set = tokenizer.sep_token is not None
    is_cls_token_set = tokenizer.cls_token is not None
    is_pad_token_set = tokenizer.pad_token is not None
    is_eos_token_set = tokenizer.eos_token is not None

    with open(file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                item = json.loads(line.strip())
                input = item["input"]
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
                labels.append(item["target"])
            except json.JSONDecodeError as e:
                print(f"Error: JSON decoding failed - {e}")
                continue
    logging.info(f"Skipped {skipped} samples due to special tokens")

    return comments, codes


def mrr(model, tokenizer, file, args):
    random.seed(42)

    # load data
    comments, codes = load_data_for_mrr(tokenizer, file)

    # create mrr chunks with (default 99) distractors

    chunks = []
    for i, sample in enumerate(zip(comments, codes)):
        comment, code = sample
        codes_without_sample = codes[:i] + codes[i + 1 :]
        # select 99 random codes
        distractors = random.sample(codes_without_sample, args.distractors)
        # create samples
        codes = [code] + distractors
        comments = [comment] * len(codes)
        labels = [1] + [0] * len(distractors)
        # convert to features
        features = _convert_examples_to_features(
            comments,
            codes,
            labels,
            tokenizer=tokenizer,
            max_seq_length=args.seq_len,
            cls_token=tokenizer.cls_token,
            sep_token=tokenizer.sep_token,
            cls_token_segment_id=tokenizer.cls_token_id,
            pad_token_segment_id=tokenizer.pad_token_id,
            eos_token=tokenizer.eos_token,
        )

        chunks.append(features)

    # make predictions for all chunks
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)
    model.to(device)
    model.eval()

    ranks = []
    for chunk in tqdm(chunks):
        # calc correct sample (always the first one)
        correct = chunk[0]
        input_ids = correct["input_ids"].unsqueeze(0).to(device)
        attention_mask = correct["attention_mask"].unsqueeze(0).to(device)
        labels = correct["labels"].unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            logits = outputs.logits
            correct_score = logits[0][0].item()

        # calc scores for the rest of the samples
        scores = []
        # add correct score to scores
        scores.append(correct_score)
        # create batches of size args.batch_size
        batch_size = args.batch_size
        for i in range(1, len(chunk), batch_size):
            batch = chunk[i : i + batch_size]
            input_ids = torch.stack([sample["input_ids"] for sample in batch]).to(device)
            attention_mask = torch.stack([sample["attention_mask"] for sample in batch]).to(device)
            labels = torch.stack([sample["labels"] for sample in batch]).to(device)
            with torch.no_grad():
                outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
                logits = outputs.logits
                scores.extend(logits[:, 1].cpu().numpy().tolist())

        rank = np.sum(np.array(scores) >= correct_score)
        ranks.append(rank)

    mean_mrr = np.mean(1.0 / np.array(ranks))

    return mean_mrr


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
    parser.add_argument("--distractors", type=int, default=99, help="number of distractors per true pair")
    parser.add_argument("--log_level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")

    args = parser.parse_args()

    TRAIN_FILE = "./codesearchnet_adv/train_adv_clf.jsonl"

    # logging
    logging.basicConfig(level=args.log_level)

    # load tokenizer
    logging.info("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(args.model)

    # load data
    logging.info("Loading data...")
    dataloader = load_data(tokenizer, args.batch_size, args.seq_len, TRAIN_FILE)

    model = AutoModelForSequenceClassification.from_pretrained(args.model)

    # train
    logging.info("Training...")
    train(model, dataloader, args)

    # save model
    logging.info("Saving model...")
    model.save_pretrained(f"{args.output_dir}/{args.model}")
    # also soave tokenizer
    tokenizer.save_pretrained(f"{args.output_dir}/{args.model}")

    DS_FOLDER = "./"

    FILES = [
        ["statcodesearch", "test_statcodesearch"],
        ["codesearchnet_adv", "test_adv"],
        ["codesearchnet_go", "test_go"],
        ["codesearchnet_java", "test_java"],
        ["codesearchnet_javascript", "test_javascript"],
        ["codesearchnet_php", "test_php"],
        ["codesearchnet_ruby", "test_ruby"],
        ["cosqa", "test_cosqa"],
    ]

    results = {}
    for meta_data in FILES:
        logging.info(f"Evaluating on {meta_data}...")
        metrics = mrr(model, tokenizer, f"{DS_FOLDER}/mrr/{meta_data[0]}/{meta_data[1]}_mrr.jsonl", args)
        results[meta_data[0]] = metrics
        logging.info(f"Test results for {meta_data}: {metrics}")

    logging.info(f"Test results: {results}")


if __name__ == "__main__":
    main()
