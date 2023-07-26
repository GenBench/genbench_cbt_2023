# Cross Lingual Consistency

## Abstract
*Copy the abstract of your accompanying paper for this task here Cross Lingual Consistency.*
Multilingual large-scale Pretrained Language Models (PLMs) have been shown to learn considerable amounts of factual knowledge from the training corpora. However, large variations are observed in the extent to which this knowledge generalizes across different languages. With the ultimate goal of ensuring that users with different language backgrounds obtain consistent feedback from the same model, we study the cross-lingual consistency (CLC) of factual knowledge in various multilingual PLMs. To this end, we resplit the existing mLAMA (Kassner et al., 2021) to construct a new benchmark BMLAMA where instances for each language are balanced. Additionally, we propose a new Ranking-based Consistency (RankC) metric to evaluate knowledge consistency across languages independently from accuracy. We conduct an in-depth analysis of the determining factors for CLC, both at model level and at language-pair level. Among other results, we find that average CLC is low across different PLMs. Moreover, increasing model size leads to higher factual probing accuracy in most languages, but does not improve cross-lingual consistency. All code and data released at https://anonymized.

## Statistics of the Balanced Multilingual LAMA (BMLAMA)
Property			|	BMLAMA-17	|	BMLAMA-53
\# Language			|	17			|	53
\# Relations		|	41			|	30
\# Queries			|	6792*17		|	3070*53
\# Candidates (Avg)	|	9.71		|	9.56

## Examples
*Give some examples of the Cross Lingual Consistency.*
Instead of measuring the amount of factual knowledge encoded in each language, we focus on its consistency across languages, which shows how knowledge is generalized among different languages in the PLM.
As illustrated in Figure Motivation (see motivation.png), the multilingual Bloom-3b model outputs consistently correct completions of the first prompt when queried in English, Spanish, and Vietnamese, but not in Hungarian and Greek.
The model also outputs consistent, though wrong, answers to the second query in English, Spanish, and Vietnamese (but not in Hungarian and Greek), suggesting the first three languages share relevant knowledge representations within the model.

## Data Source
*Describe the data source for this Cross Lingual Consistency.*
BMLAMA is filtered from mLAMA, where the number of queries for different languages are balanced.
We first probing the PLMs with same questions in all supported languages and record the rankings of all candidates.
Based on the ranking lists of two languages (e.g. en and es), we propose RankC metric to compute the cross-lingual consistency of factual knowledge between different language pairs.

## Usage
*Describe how to load your task and what is required for evaluation, if anything.*
We provided one example in "test.jsonl". For more recorded candidate rankings, see folder 'record17' and 'record53'.

Using the "format\_example()" function, we show the rankings of candidates when probing Bloom-3b with en and es queries in BMLAMA. 
We also write the RankC metric in the same function to output the cross-lingual consistency of factual knowledge between these two languages.
For full CLC results on BMLAMA-17 with Bloom-3b, see 'bloom\_3b\_CLC.png'.


## Limitations and Bias
*Note any known limitations or biases that the Cross Lingual Consistency has, with links and references if possible.*
Limitation:
Due to restriction of our GPU resources, we could not test models larger than Bloom-3b. Extending our analysis to larger-scale models in future work is encouraged to see if the same conclusions reached. Nevertheless, results in the paper indicate that the average CLC grows extremely slowly with the increment of model scale.

The facts included in BMLAMA, while supposed to be universals, are likely to be more relevant to the Western world, which can introduce a bias in the evaluation. We inherit this problem from the benchmarks BMLAMA is built upon. Fixing this issue is not trivial, especially in comparative work where probing the exact set of facts across languages is a requirement, and should be given attention in future work.

Bias:
Since BMLAMA data is derived from previous works X-FACTR and MLAMA, queries in BMLAMA are also likely to encounter gender and racial bias issues, which are inevitable in the source Wikidata. However, this paper mostly focuses on the consistency between knowledge in different languages rather than the specific knowledge in a single language.

## GenBench Eval card
*Describe what kind of generalisation your task is evaluating, and include a [genbench eval card](https://genbench.org/eval_cards/) for your task*.
(See eval\_card.png)
