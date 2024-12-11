
def get_jsonnet(language, split, has_dev):
    return f"""{{
    name: 'mSCAN (language: {language}, split: {split})',

    // @TODO: Add a description of the task
    description: 'Multilingual SCAN ({language}) aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'keyword1',
        'keyword2',
    ],

    authors: [
        'Amélie Reymond',
        'Shane Steinert-Threlkeld',
    ],

    data_source: {{
        type: 'manual',
        train: 'https://huggingface.co/datasets/ameliettr/mSCAN/raw/main/{language}/{split}/train.jsonl',
        test: 'https://huggingface.co/datasets/ameliettr/mSCAN/raw/main/{language}/{split}/test.jsonl',
        {f"validation: 'https://huggingface.co/datasets/ameliettr/mSCAN/raw/main/{language}/{split}/dev.jsonl'," if has_dev else ""}
    }},

    has_validation_set: {"true" if has_dev else "false"},
    has_train_set: true,

    task_type: 'free_form',

    preparation_strategies: {{
        finetuning: {{
            objective: 'maximum_likelihood',
        }},

        prompt_based_testing: {{
            prompt_builder: {{
                instruction_zero_shot: '',
                input_prefix: 'IN: ',
                output_prefix: 'OUT: ',
                append_choices_to_input: false,
                few_shot_example_separator: '\\n\\n',
                stop_string: '\\n\\n',
            }}
        }},

    }},

    evaluation_metrics: [
        {{
            hf_id: 'exact_match',
            git_commit_sha: "758135da6a37ce962b7bc38c6dd5eab672d2b742",
            best_score: 1.0,
        }}
    ]
}}"""


languages = ["cmn", "eng", "fra", "hin", "rus"]
splits = {
    "add_prim_jump": {
        "has_dev": False
    },
    "add_prim_turn_left": {
        "has_dev": False
    },
    "length": {
        "has_dev": False
    },
    "mcd1": {
        "has_dev": True
    },
    "mcd2": {
        "has_dev": True
    },
    "mcd3": {
        "has_dev": True
    },
    "simple": {
        "has_dev": False
    },
}

for language in languages:
    for split_name, split_args in splits.items():
        jsonnet = get_jsonnet(language, split_name, split_args["has_dev"])
        with open(f"src/genbench/tasks/mscan/{language}_{split_name}/config.jsonnet", "w") as f:
            f.write(jsonnet)

