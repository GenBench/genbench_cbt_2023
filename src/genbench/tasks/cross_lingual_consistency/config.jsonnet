{
    name: 'Cross Lingual Consistency',

    // @TODO: Add a description of the task
    description: 'Cross Lingual Consistency aims to measure ...',

    // @TODO: Add a list of keywords that describe the task
    keywords: [
        'Model Consistency', 
		'Multilinguality',
		'Knowledge Incorporation', 
		'Large-scale Pre-trained Language Model', 
		'Model Evaluation', 
		'Knowledge Probing',
    ],

    authors: [
        'Jirui Qi',
        'Raquel Fernández',
        'Arianna Bisazza',
        
    ],

    data_source: {
        type: 'manual',
		BMLAMA17: 'https://raw.githubusercontent.com/Betswish/genbench_cbt/BMLAMA/src/genbench/tasks/cross_lingual_consistency/BMLAMA17/',
		BMLAMA53: 'https://raw.githubusercontent.com/Betswish/genbench_cbt/BMLAMA/src/genbench/tasks/cross_lingual_consistency/BMLAMA53/',
		test: 'https://placeholder'
    },
	

    has_validation_set: false,
    has_train_set: false,

    task_type: 'multiple_choice',

    field_mapping: {
        input: 'Prompt',
        target: 'Ans',
		target_options: 'Candidate Ans',
    },

    evaluation_metrics: [
    ],

    preparation_strategies: {
        // A recipe for preparing the model to perform the task by configuring its prompt.
        // This recipe is suitable for generative LMs such as GPT-3, OPT, T5, etc.
        // We provide a few options for configuring the prompt. But, the task creator can
        // also provide a custom prompt preparation in the task's Python class.
    },
}
