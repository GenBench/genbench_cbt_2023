{
    name: 'Natural Language Codesearch Classification (codesearchnet_ruby)',

    description: 'Natural Language Codesearch Classification (codesearchnet_ruby) aims to measure the generalization capabilites of language models in code understanding. This subtasks measures cross-lingual generalization',

    keywords: [
        'codesearch',
        'natural language query',
        'binary classification',
        'ruby',
        'cross-lingual'
    ],

    authors: [
        'Andor Diera',
        'Abdelhalim Dahou',
		'Lukas Galke',
		'Fabian Karl',
        'Florian Sihler',
		'Ansgar Scherp',        
    ],

    data_source: {
        type: 'manual',
        test: 'https://zenodo.org/record/8310891/files/test_ruby.jsonl',
        train:'https://zenodo.org/record/8310891/files/train_adv.jsonl',
    },

    has_validation_set: false,
    has_train_set: true,

    task_type: 'multiple_choice',

    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            git_commit_sha: '34d6add55811828baef83e0d7c6826e2193f7b6a',
            best_score: 1.0,
        },
    ],

    preparation_strategies: {
        finetuning: {
            objective: 'maximum_likelihood',
        },
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: 'Given a code comment and a Ruby programming language code snippet, determine if the comment accurately represents the function of the code. Respond with True if the code matches the comment and False if it does not. The input format is defined as comment [CODESPLIT] code',
                input_prefix: '',
                output_prefix: '',
                choices_prefix: '',
                append_choices_to_input: false,
            }
        },
    },
}