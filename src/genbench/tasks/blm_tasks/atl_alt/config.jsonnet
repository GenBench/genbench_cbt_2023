{
    name: 'BLM_tasks (atl_alt)',

    description: 'BLM_tasks (atl_alt) aims to measure the detection of rules related to spray/load verb alternations in neural networks. The dataset was automatically generated based on manually collected seeds and predefined patterns, and using overlapping generation rules that combine different syntactic-semantic properties relevant to verb alternations.',

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
    train: 'https://raw.githubusercontent.com/CLCL-Geneva/GenBench/main/BLMs/ATL-ALT_train.jsonl',
    test: 'https://raw.githubusercontent.com/CLCL-Geneva/GenBench/main/BLMs/ATL-ALT_test.jsonl',
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
