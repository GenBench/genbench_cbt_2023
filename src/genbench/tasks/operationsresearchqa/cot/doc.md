# OperationsResearchQA (cot)

## Summary

**ORQA: Can Pretrained Language Models reason about Operations Research?**

We propose Operations Research QA (ORQA) as a new benchmark to evaluate the ability of pretrained Large Language Models (LLMs) to generalize to new technical domains. Our benchmark considers the cross-domain shift issue of LLMs and focuses on the multi-choice question answering task. In our new dataset, the target domain is Operations Research (OR), and the task tests both the language models' domain-specific knowledge and reasoning skills on optimization modeling. Our dataset is handcrafted by domain experts, i.e. OR experts, and is representative of different types of optimization and various application domains, such as vehicle routing, production planning, or investment portfolio allocation.

We contribute a novel multi-choice QA dataset for specialized technical domains. Each instance of the dataset contains the following:

1. An `input` context describing an optimization model as a case study.
2. A `question` asking about the understanding of the problem specifications (e.g. objective criterion or constraints), the underlying components of the corresponding optimization model (e.g. the elements participating in the optimization), as well as the structure and logic of the optimization model (e.g. the logical relation between two decision activities).
3. A list of `options` for the answer, which was handcrafted by OR experts to make the question challenging to guess. The LLM must select the correct answer from a list of four options.
4. The correct `target` answer.
5. For chain-of-thoughts, there is a `reasoning` field. Please refer to the accompanying paper submission for more details.

It is important to emphasize that each question is designed to require basic knowledge of optimization, an understanding of the problem description, and, more importantly, multi-step reasoning. We have selected the field of operations research due to the high level of technical expertise required to understand and answer questions about optimization modeling.

We have carefully selected the optimization problems from various domains. Furthermore, each question/choice/answer instance has been curated and verified by domain experts. As a result, ORQA is positioned to be an impactful benchmark that can contribute to the evaluation of general-purpose LLMs' generalization ability on specialized domains and tasks.

CoT is performed in a two-step approach with first a reasoning-eliciting prompt followed by an anser-eliciting prompt. Please refer to the accompanying paper for more details.

## Motivation

Our proposed Operations Research Question Answering (ORQA) benchmark is highly relevant to the GenBench collaborative task, as it addresses the crucial aspect of generalization in natural language processing (NLP) models. Specifically focused on pretrained Large Language Models (LLMs) within the domain of Operations Research (OR), ORQA is designed to tackle the significant cross-domain shift issue. By presenting a multi-choice question answering task that tests reasoning skills and domain-specific knowledge in optimization modeling, ORQA provides a comprehensive evaluation platform.

As the first benchmark of its kind in Operations Research, ORQA serves as an open and collaborative platform to assess LLMs' real-world performance in specialized technical domains. The primary goal is to ensure responsible and well-informed deployment of LLMs, minimizing potential negative impacts. Notably, unlike technical reports from commercial LLM vendors, ORQA is an open-source benchmark, ensuring impartiality and transparency in the evaluation process. This approach aligns perfectly with our motivation to advance research on generalization in NLP and promote the responsible development of LLMs. By creating a benchmark that specifically targets optimization and Operations Research, we aim to foster a collective effort within the NLP community, enhancing the reliability and practical applicability of LLMs in professional domains.

## Examples

Please refer to the data section (Section 4) and the appendix of the accompanying paper for some more examples. Here is one example:

**<u>EXAMPLE 1</u>**

**Context:**

In the bustling district of Paris lies \"La Douceur Parisienne,\" a patisserie celebrated for its exquisite pastries. Mademoiselle Elise, the owner, finds herself in a perpetual balancing act, juggling the freshness of her products with the economics of running her establishment. Every item on her display boasts a distinct shelf life, determining its freshness window. Once this period lapses, the product is no longer up to the patisserie's esteemed standards.  When Mademoiselle Elise places an order for ingredients, a fixed cost is immediately incurred. This cost isn't just a function of the quantity but also of the unique suppliers she sources her premium ingredients from. Alongside this, the selling price of each pastry, when weighed against the purchase cost of its ingredients, paints a picture of the potential profit for every item sold.  However, there's an inherent challenge in procuring these ingredients. They come in defined batches, meaning even if she needs a smaller quantity, the entire batch must be ordered. This batching can sometimes lead to an excess, posing a risk given the perishable nature of her products.  Furthermore, the streets of Paris, with their unpredictable nature, bring another layer of complexity. On some days, a burst of tourists might grace her establishment, while on others, only the familiar faces of locals appear. This ebb and flow in demand means that her ingredient orders must be agile, flexible, and well-timed.  With these intricate challenges, Mademoiselle Elise's mission is clear: to craft an ordering strategy that efficiently straddles between reducing costs from ordering, potential waste, and maximizing sales revenue. Through this balanced approach, she hopes to ensure that every day at \"La Douceur Parisienne\" commences with fresh, impeccable pastries and ends on a note of robust profitability.

**Question:**

What is the type of optimization model related to this problem?

**Reasoning:**

Mademoiselle Elise's objective is to balance costs, potential waste, and maximize sales revenue in her patisserie.\r\nThere are multiple variables to consider, such as ingredient costs, pastry selling prices, and varying demand.\r\nThe problem requires accommodating constraints like fixed ordering costs, perishability of products, batching of ingredients, and unpredictable customer flow.\r\nDespite the complexities, the relationships among these variables and constraints appear to be linear.\r\nBased on the nature of the problem and the linearity of the relationships, the most appropriate optimization model is Linear Programming.\r\nAnswer: (B) Linear Programming.

**Target:**

1

**Target Options:**

0: Power Cone Programming

1: Linear Programming

2: Non-Linear Programming

3: Exponential Cone Programming



## Usage

The task can be loaded by calling `genbench_cbt\src\cot_inference.py`. This script goes through an inference and evaluation cycle of the standard prompts. It currently supports using the OpenAI API and HuggingFace API. You may alter the code to run inference using an LLM of your choice.

## Data Source

The data creation process is better defined in the accompany paper. The dataset is separated into validation and testing splits with 30 and 1483 samples, respectively. These can be accessed at the following links:

Test - https://raw.githubusercontent.com/OpResearchQA/ORQA_data/main/test_dataset.jsonl

Validation - https://raw.githubusercontent.com/OpResearchQA/ORQA_data/main/val_dataset.jsonl

## Limitations and Bias

Any decision-making problem may be formulated as an optimization model. Thus, the field of OR spans all domains and it is infeasible for our dataset to comprehensively represent all domains. This benchmark is limited by the coverage of domains as it targets more common domains of OR.

## GenBench Eval card

The GenBench Eval card is the same as for the parent ORQA task. These subtasks are to separate the two approaches of standard v. CoT prompting.
