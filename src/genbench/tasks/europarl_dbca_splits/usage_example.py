"""
Usage example for the Europarl DBCA splits task.

Training of the NMT model is mostly based on the HuggingFace NLP course chapter on translation:
https://huggingface.co/learn/nlp-course/chapter7/4?fw=pt
"""
import argparse
from genbench import load_task
from genbench.api import PreparationStrategy
from datasets import DatasetDict
from transformers import FSMTConfig, FSMTTokenizer, FSMTForConditionalGeneration, pipeline
from transformers import DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer


def tokenize_corpus(dataset, save_to_file):
    """
    Tokenizes the dataset and saves it to disk.
    """
    def preprocess_function(examples):
        inputs = examples["input"]
        targets = examples["target"]
        model_inputs = tokenizer(
            inputs, text_target=targets, max_length=MAX_LENGTH, truncation=True
        )
        return model_inputs

    dataset = DatasetDict(dataset)
    tokenized = dataset.map(
        preprocess_function,
        batched=True,
    )
    tokenized.save_to_disk(save_to_file)
    return tokenized


def translate_sentences(model_name_or_path, eval_dataset):
    """
    Translates the sentences in eval_dataset using the given model.
    """
    translator = pipeline(
        "translation",
        model=model_name_or_path,
        device="cuda",
        batch_size=BATCH_SIZE,
    )
    return translator(eval_dataset, max_length=MAX_LENGTH)


def train_from_scratch(tokenized_corpus, output_dir_name):
    """
    Trains an FSMT model from scratch.
    Model architecture is similar to that in Vaswani et al. (2017).
    """
    config = FSMTConfig(
        activation_dropout=0.0,
        activation_function="relu",
        architectures=["FSMTForConditionalGeneration"],
        attention_dropout=0.1,
        bos_token_id=0,
        d_model=512,
        decoder={
            "bos_token_id": 2,
            "model_type": "fsmt_decoder",
            "vocab_size": 42024
        },
        decoder_attention_heads=8,
        decoder_ffn_dim=2048,
        decoder_layerdrop=0,
        decoder_layers=6,
        decoder_start_token_id=2,
        dropout=0.1,
        encoder_attention_heads=8,
        encoder_ffn_dim=2048,
        encoder_layerdrop=0,
        encoder_layers=6,
        eos_token_id=2,
        forced_eos_token_id=2,
        init_std=0.02,
        is_encoder_decoder=True,
        langs=["en", "de"],
        length_penalty=1.15,
        max_length=MAX_LENGTH,
        max_position_embeddings=1024,
        model_type="fsmt",
        num_beams=5,
        num_hidden_layers=6,
        pad_token_id=1,
        scale_embedding=True,
        src_vocab_size=42024,
        tgt_vocab_size=42024,
        tie_word_embeddings=False,
        transformers_version="4.35.2",
        use_cache=True,
    )
    model = FSMTForConditionalGeneration(config=config)

    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir_name,
        evaluation_strategy="steps",
        eval_steps=5000,
        save_strategy="steps",
        save_steps=10000,
        learning_rate=2e-5,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        weight_decay=0.01,
        save_total_limit=10,
        max_steps=100000,
        fp16=True,
    )

    trainer = Seq2SeqTrainer(
        model,
        training_args,
        train_dataset=tokenized_corpus["train"],
        eval_dataset=tokenized_corpus["validation"],
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    trainer.train()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--tokenize", action="store_true")
    argparser.add_argument("--train", action="store_true")
    argparser.add_argument("--eval", action="store_true")
    args = argparser.parse_args()

    # Load the task
    task = load_task('europarl_dbca_splits')

    # A pretrained multilingual tokenizer, used for both models and both languages
    tokenizer = FSMTTokenizer.from_pretrained('stas/tiny-wmt19-en-de')

    MAX_LENGTH = 128
    BATCH_SIZE = 128

    results = []
    # "comdiv0" is the easy non-compositional data split, with minimal compound divergence
    # "comdiv1" is the difficult, compositional data split, with maximal compound divergence
    # English-German corpus is used for this example.
    # For other target languages, replace "de" with "fr", "el", or "fi" in the subtask name.
    for comdiv in ["0", "1"]:
        if comdiv == "0":
            subtask = task.comdiv0_de
        else:
            subtask = task.comdiv1_de

        subtask_dataset = subtask.get_prepared_datasets(PreparationStrategy.FINETUNING)

        tokenized_dataset_dir = f'ds_de_comdiv{comdiv}_tokenized'
        if args.tokenize:
            tokenized_datasets = tokenize_corpus(subtask_dataset, tokenized_dataset_dir)
        else:
            tokenized_datasets = DatasetDict.load_from_disk(tokenized_dataset_dir)

        # Extract a validation set from training set
        train_val_split = tokenized_datasets["train"].train_test_split(test_size=0.01)
        tokenized_datasets["train"] = train_val_split["train"]
        tokenized_datasets["validation"] = train_val_split["test"]

        nmt_model_dir = f'FSMT_en-de_comdiv{comdiv}'
        if args.train:
            train_from_scratch(tokenized_datasets, nmt_model_dir)

        if args.eval:
            cp = 'checkpoint-100000'
            print(f"Results for comdiv{comdiv}, checkpoint {cp}")
            preds = translate_sentences(nmt_model_dir + '/' + cp,
                                        tokenized_datasets["test"]["input"])

            # re-map the keys to match the evaluation script
            preds = [{'target': pred['translation_text']} for pred in preds]

            score = subtask.evaluate_predictions(
                        predictions=preds,
                        gold=tokenized_datasets["test"],
                    )
            print(score)
            results.append(score)

    if args.eval:
        print('Generalisation score (maximum compound divergence score divided by ' \
                + 'minimum compound divergence score):')
        print(results[1]['hf_chrf__score'] / results[0]['hf_chrf__score'])
