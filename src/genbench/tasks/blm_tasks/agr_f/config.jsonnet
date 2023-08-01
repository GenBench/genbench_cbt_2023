{
    name: 'BLM_tasks (agr_f)',


    description: 'BLM_tasks (agr_f) aims to measure the detection of rules related to the subject-verb agreement (in French) in neural networks. The dataset was automatically generated based on manually collected seeds and predefined patterns, and using overlapping generation rules that combine different number of attractors and grammatical numbers for NPs and verbs',
	
	  keywords: [
	    'rule-like generalization',
	    'underlying problem structure',
	    'grammatical phenomena',
	    'subject-verb agreement',
	    'French',
	  ],
  
    authors: [
        'Paola Merlo',
        'Chunyang Jiang',
        'Aixiu An',
        'Maria A. Rodriguez',
        'Vivi Nastase',
    ],

  data_source: {
    type: 'manual',
    train: 'https://raw.githubusercontent.com/CLCL-Geneva/GenBench/main/BLMs/agrF_train.jsonl',
    test: 'https://raw.githubusercontent.com/CLCL-Geneva/GenBench/main/BLMs/agrF_test.jsonl',
  },

  has_validation_set: false,
  has_train_set: true,

  task_type: 'multiple_choice',

  field_mapping: {
    input: 'input',
    target: 'target',
    target_options: 'target_options',
  },

  evaluation_metrics: [
    {
      hf_id: 'f1',
      git_commit_sha: '3a4c40f7397dcd7d9dccf0659616dc6b14072dcb',
      best_score: 1.0,      
    },
  ],

  preparation_strategies: {
    finetuning: {
      objective: 'maximum_likelihood',
    },
  },

}
