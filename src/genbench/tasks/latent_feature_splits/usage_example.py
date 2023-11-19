from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer, DataCollatorWithPadding, \
    Trainer, TrainingArguments,  AutoModelForSequenceClassification
import numpy as np
import evaluate
from genbench import load_task
from genbench.api import PreparationStrategy
import os


def compute_metrics(eval_preds):
    metric = evaluate.load("f1")
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(
        predictions=predictions,
        references=labels,
        average="macro")


def main(split_name, num_labels, bsz, lr, epochs, checkpoint):
    """
    Basic functionality to load data, train and evaluate the model.
    Args:
        - split_name: str (bert_closest_split | roberta_closest_split)
        - num_labels (int)
        - bsz (int): batch size
        - lr (float): learning rate
        - epochs (int): number of epochs
        - checkpoint (str): should be a valid HF model name
    """

    def tokenize_function(example):
        return tokenizer(
            example["input"])

    # Convert GenBench format to HF dataset format, preview dataset
    task = load_task(f"latent_feature_splits:{split_name}")
    ds = task.get_prepared_datasets(PreparationStrategy.FINETUNING)
    ds = DatasetDict(ds)
    ds = ds.rename_column("target", "label")
    print(ds)

    # Load and preprocess data
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    tokenized_datasets = ds.map(
        tokenize_function, batch_size=bsz, batched=True)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # Load model and HF trainer, WITH evaluation during training
    model = AutoModelForSequenceClassification.from_pretrained(
        checkpoint, num_labels=num_labels)
    training_args = TrainingArguments(
        "test-trainer",
        learning_rate=lr,
        num_train_epochs=epochs,
        per_device_train_batch_size=bsz,
        per_device_eval_batch_size=bsz,
        evaluation_strategy="epoch")
    trainer = Trainer(
        model,
        training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # Evaluate for random performance level, train, evaluate again
    predictions = trainer.predict(tokenized_datasets["test"])
    f1_pre = compute_metrics((predictions.predictions, predictions.label_ids))
    trainer.train()
    predictions = trainer.predict(tokenized_datasets["test"])
    f1_post = compute_metrics((predictions.predictions, predictions.label_ids))
    print(f"Random f1: {f1_pre}, f1 post-training: {f1_post}")



if __name__ == "__main__":
    os.environ["WANDB_DISABLED"] = "true"
    split_name = "bert_closest_split"
    num_labels = 3
    batch_size = 16
    lr = 3e-5
    epochs = 5
    checkpoint = "prajjwal1/bert-small"

    main(split_name, num_labels, batch_size, lr, epochs, checkpoint)
