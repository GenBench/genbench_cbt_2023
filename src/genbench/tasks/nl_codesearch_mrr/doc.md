## Motivation
Language models can serve as a valuable tool for software developers to increase productivity. Large generative models can be used for code generation and code completion, while smaller encoder-only models are capable of performing code search tasks using natural language queries. These capabilities are heavily influenced by the quality and diversity of the available training data. Source code datasets used for training usually focus on the most popular languages and testing is mostly conducted on the same distributions, often overlooking low resource programming languages. Motivated by the NLP generalisation taxonomy proposed by Hupkes et. al., we propose a new benchmark dataset called [placeholder] which builds upon existing natural language code search datasets to systemically study the code understanding generalization capabilities of language models. For evaluation and comparison, we collect several baseline results using fine-tuned BERT-style models and GPT-style large language models in a zero-shot setting.

## Examples
Given n number of code comment pairs (1 true pair and n-1 distractor pair where a comment has been matched with a random code snippet), calculate the MRR score.

true sample: {"input": "Allocate sampled topics to the documents rather than estimate them . Automatically generate term - topic and document - topic matrices . [SEP] def set_sampled_topics ( self , sampled_topics ) : assert sampled_topics . dtype == np . int and len ( sampled_topics . shape ) <= 2 if len ( sampled_topics . shape ) == 1 : self . sampled_topics = sampled_topics . reshape ( 1 , sampled_topics . shape [ 0 ] ) else : self . sampled_topics = sampled_topics self . samples = self . sampled_topics . shape [ 0 ] self . tt = self . tt_comp ( self . sampled_topics ) self . dt = self . dt_comp ( self . sampled_topics )", "target": 1, "target_options": ["no_match", "match"]} \
distractor sample: {"input": "Allocate sampled topics to the documents rather than estimate them . Automatically generate term - topic and document - topic matrices . [SEP] def _resolve_entity ( mo ) : ent = mo . group ( \"entity\" ) s = mo . group ( ) if s . startswith ( '&#' ) : if s [ 2 ] in 'xX' : radix = 16 else : radix = 10 try : num = int ( ent , radix ) except ( ValueError , OverflowError ) : return u'' else : num = name2codepoint . get ( ent ) if num is None or num < 0 : # unknown entity -> ignore return u'' try : return unichr ( num ) except ValueError : return u''", "target": 0, "target_options": ["no_match", "match"]}

## Data Source
**CodeSearchNet** : original dataset first published in https://arxiv.org/pdf/1909.09436.pdf , Java, Javascript, Go, Ruby, PHP subsets collected from huggingface-hub \
**CodeSearchNet Adv** : a processed version of the CodeSearchNet Python dataset, introduced in the CodeXGLUE benchmark suite https://github.com/microsoft/CodeXGLUE \
**WebQuery** : Python codesnippets from the CodeSearchNet dataset paired with real world user search engine queries, introduced in the CodeXGLUE benchmark suite: https://github.com/microsoft/CodeXGLUE \
**StatCodeSearch** : R code-comment pair snippets, scraped and extracted from public project on the Open Science Framework (OSF) by the submission authors \

During evaluation for each true code-comment pair we create n number of distractors where the comment is matched with a random code snippet. The distractor samples are sampled consistently by setting the random seed in the get_raw_data function

**Dataset Size**:\
*Finetuning set:* \
 -CodeSearchNet Adv train set 251k \
*Test sets:* \
 -CodeSearchNet Adv test set 19k \
 -WebQuery test set 1k \
 -CodeSearchNet Ruby test set 2k \
 -CodeSearchNet Go test set 14k \
 -CodeSearchNet Java test set 26k \
 -CodeSearchNet Javascript test set 6k \
 -CodeSearchNet PHP test set 28k \
 -StatCodeSearch test set TBD 
## Limitations and Bias
TBD

## Citation
TBD

## Further References
@article{husain2019codesearchnet,
  title={Codesearchnet challenge: Evaluating the state of semantic code search},
  author={Husain, Hamel and Wu, Ho-Hsiang and Gazit, Tiferet and Allamanis, Miltiadis and Brockschmidt, Marc},
  journal={arXiv preprint arXiv:1909.09436},
  year={2019}
} \
@article{Lu2021CodeXGLUEAM,
  title={CodeXGLUE: A Machine Learning Benchmark Dataset for Code Understanding and Generation},
  author={Shuai Lu and Daya Guo and Shuo Ren and Junjie Huang and Alexey Svyatkovskiy and Ambrosio Blanco and Colin Clement and Dawn Drain and Daxin Jiang and Duyu Tang and Ge Li and Lidong Zhou and Linjun Shou and Long Zhou and Michele Tufano and Ming Gong and Ming Zhou and Nan Duan and Neel Sundaresan and Shao Kun Deng and Shengyu Fu and Shujie Liu},
  journal={ArXiv},
  year={2021},
  volume={abs/2102.04664}
*}
