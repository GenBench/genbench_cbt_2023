"""
Run using:

python -m genbench.tasks.bias_amplified_splits.wanli.usage_example --max_train_samples 10000

"""
import logging
import argparse
import numpy as np

import evaluate
from datasets import (
    DatasetDict,
    ClassLabel,
)
from transformers import (
    AutoModelForSequenceClassification,
    AutoConfig,
    AutoTokenizer,
    DataCollatorWithPadding,
    EvalPrediction,
    Trainer,
    TrainingArguments,
)

from genbench import load_task
from genbench.api import PreparationStrategy


task_to_keys = {
    "mnli": ("premise", "hypothesis"),
    "wanli": ("premise", "hypothesis"),
    "qqp": ("question1", "question2"),
}
task_to_labels = {
    "mnli": ("entailment", "neutral", "contradiction"),
    "wanli": ("entailment", "neutral", "contradiction"),
    "qqp": ("not_duplicate", 'duplicate'),
}
task_to_label_col = {
    "mnli": "label",
    "wanli": "gold",
    "qqp": "label",
}

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name_or_path", type=str, default="roberta-base")
    parser.add_argument("--task_name", type=str, default="wanli")
    parser.add_argument("--num_train_epochs", type=int, default=1)
    parser.add_argument("--per_device_train_batch_size", type=int, default=8)
    parser.add_argument("--per_device_eval_batch_size", type=int, default=16)
    parser.add_argument("--max_seq_length", type=int, default=128)
    parser.add_argument("--learning_rate", type=float, default=1e-5)
    parser.add_argument("--max_train_samples", type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )

    # Loading the dataset
    task = load_task(f"bias_amplified_splits:{args.task_name}")
    raw_datasets = task.get_prepared_datasets(
        PreparationStrategy.FINETUNING,
        shot_list=[0]
    )

    # Cast data to Dataset format
    raw_datasets = DatasetDict(raw_datasets)
    if task_to_label_col[args.task_name] != 'label':
        raw_datasets = raw_datasets.rename_column(task_to_label_col[args.task_name], 'label')
    if not isinstance(raw_datasets['train'].features['label'], ClassLabel):
        raw_datasets = raw_datasets.cast_column('label', ClassLabel(num_classes=len(task_to_labels[args.task_name]), names=task_to_labels[args.task_name]))
    label_list = task_to_labels[args.task_name]
    num_labels = len(label_list)

    # Load pretrained model and tokenizer
    config = AutoConfig.from_pretrained(
        args.model_name_or_path,
        num_labels=num_labels,
        finetuning_task=args.task_name,
    )
    tokenizer = AutoTokenizer.from_pretrained(
        args.model_name_or_path,
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model_name_or_path,
        config=config,
    )

    # Preprocessing the raw_datasets
    sentence1_key, sentence2_key = task_to_keys[args.task_name]

    def preprocess_function(examples):
        # Tokenize the texts
        inputs = (
            (examples[sentence1_key],) if sentence2_key is None else (examples[sentence1_key], examples[sentence2_key])
        )
        result = tokenizer(*inputs, padding=True, max_length=args.max_seq_length, truncation=True)
        return result

    raw_datasets = raw_datasets.map(
        preprocess_function,
        batched=True,
        desc="Running tokenizer on dataset",
    )

    train_dataset = raw_datasets["train"]
    eval_dataset = raw_datasets["validation"]
    test_dataset = raw_datasets["test"]

    if args.max_train_samples is not None:
        max_train_samples = min(len(train_dataset), args.max_train_samples)
        train_dataset = train_dataset.select(range(max_train_samples))

    # Get the metric function
    acc_metric = evaluate.load("accuracy")
    f1_metric = evaluate.load("f1")

    def compute_metrics(p: EvalPrediction):
        preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
        preds = np.argmax(preds, axis=1)
        acc = acc_metric.compute(predictions=preds, references=p.label_ids)
        f1 = f1_metric.compute(predictions=preds, references=p.label_ids, average="macro")
        result = acc | f1
        return result

    # Initialize our Trainer
    training_args = TrainingArguments(
        f"runs/bias_amplified_splits/{args.task_name}",
        learning_rate=args.learning_rate,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        evaluation_strategy="epoch",
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics,
        tokenizer=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer),
    )

    logger.info("*** Train ***")
    trainer.train()

    logger.info("*** Evaluate ***")

    eval_splits = ["dev", "test"]
    eval_datasets = [eval_dataset, test_dataset]
    eval_results = dict()

    for eval_dataset, eval_split in zip(eval_datasets, eval_splits):
        eval_results[eval_split] = trainer.evaluate(eval_dataset=eval_dataset)

    logger.info(f"*** dev results (biased test set) ***")
    logger.info(f"biased accuracy: {eval_results['dev']['eval_accuracy']}")
    logger.info(f"biased macro F1: {eval_results['dev']['eval_f1']}")
    logger.info(f"*** test results (anti-biased test set) ***")
    logger.info(f"anti-biased accuracy: {eval_results['test']['eval_accuracy']}")
    logger.info(f"anti-biased macro F1: {eval_results['test']['eval_f1']}")


if __name__ == "__main__":
    main()
