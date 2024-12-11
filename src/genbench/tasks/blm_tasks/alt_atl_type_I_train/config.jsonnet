{
    name: 'BLM_tasks (alt_atl_type_I_train)',

    description: 'BLM_tasks (alt_atl_type_I_train) aims to measure the detection of rules related to spray/load verb alternation in neural networks. The dataset was automatically generated based on manually collected seeds and predefined patterns, and using overlapping generation rules that combine different syntactic-semantic properties relevant to verb alternations. Compared to the alt_atl task, the training data for this subtask has minimal lexical variation both among the sentences in the input sequence, and between the input and output sentences.',

	keywords: [
	    'rule-like generalization',
	    'underlying problem structure',
	    'grammatical phenomena',
	    'spray/load verb alternation',
	    'English',
	  ],
  
    authors: [
        'Paola Merlo',
        'Chunyang Jiang',
        'Giuseppe Samo',
        'Vivi Nastase',      
    ],

  data_source: {
    type: 'manual',
    train: 'https://raw.githubusercontent.com/CLCL-Geneva/GenBench/main/BLMs/ALT-ATL_typeI_train.jsonl',
    test: 'https://raw.githubusercontent.com/CLCL-Geneva/GenBench/main/BLMs/ALT-ATL_test.jsonl',
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
