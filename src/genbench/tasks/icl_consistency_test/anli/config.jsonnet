{
    name: 'ICL consistency test (anli)',

    description: 'The ICL consistency test measures the consistency of LLM predictions on the same datapoints across many different setups. Different setups are defined by "factors". On the one hand, factors can be specific attributes of the used prompt (e.g. the number of examples the model is presented with ["n_shots"] or the type of instructions that were used to wrap a specific datapoint ["Instructions"]). On the otherhand, the analysis can also be augmented by factors that are related to the way a model is evaluated (e.g. whether a model is calibrated) or the type of model that is evaluated (e.g. the number of parameters or instructions tuning). These external factors can be added into analysis by using the task.add_factor() method. The output-metric is Cohen\'s kappa for each factor across all different conditions. A kappa-value close to 1 indicates that the factors does not change the model prediction, while a factor close to 0 strongly changes model predictions. This test evaluates the ANLI-dataset (Nie et al., 2019).',

    keywords: [
        'consistency',
        'LLM',
        'robustness',
        'in-context learning',
        'prompt-based learning',
        'icl',
        'anli',
        'mnli'   
    ],

    authors: [
        'Lucas Weber',
        'Elia Bruni',
        'Dieuwke Hupkes',
        
    ],

    data_source: {
        type: 'manual',
        test: 'https://raw.githubusercontent.com/LucWeber/icl_consistency_data/main/data/genbench_all_anli.jsonl',  
    },

    has_validation_set: false,
    has_train_set: false,

    task_type: 'free_form',

    preparation_strategies: {
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
        prompt_based_testing: {
            prompt_builder: {
                instruction_zero_shot: '',
                instruction_few_shot: '',
                input_prefix: '',
                output_prefix: '',
            }
        },
    },
}
