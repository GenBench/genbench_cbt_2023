{
    name: 'PromptComVE',
    
        description: 'Commonsense Validation and Explanation (ComVE) is a benchmark to study the generalizability of It-LLMs towards multiple choice answers.',

    keywords: [
        'commonsense reasoning',
        'commonsense explainations',
    ],

    authors: [
        'Leonardo Ranaldi ',
        ' Giulia Pucci',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/lranaldii/Prompt-ComVE/main/data/Prompt_ComVE_t1.jsonl',
    },


    has_validation_set: false,
    has_train_set: false,
    
      field_mapping: {
    input: 'prompt',
    target: 'target',
  		},

    task_type: 'free_form',


    evaluation_metrics: [
        {
            hf_id: 'accuracy',
            git_commit_sha: '1379e97f313a00486e9885aec530e1ef00def9b9',
            best_score: 1.0,
        }
    ],

    preparation_strategies: {
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: '(following Statements), answer choise (answers)\n',
                output_prefix: '\nAnswer: ',
                input_prefix: '', // no input prefix since Question follows Context
                append_choices_to_input: false,
            }
        },
    },
}
