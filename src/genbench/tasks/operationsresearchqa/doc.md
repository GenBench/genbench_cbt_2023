# Operations Research QA (ORQA)

## Summary

**ORQA: Can Pretrained Language Models reason about Operations Research?**

We propose Operations Research QA (ORQA) as a new benchmark to evaluate the ability of pretrained Large Language Models (LLMs) to generalize to new technical domains. Our benchmark considers the cross-domain shift issue of LLMs and focuses on the multi-choice question answering task. In our new dataset, the target domain is Operations Research (OR), and the task tests both the language models' domain-specific knowledge and reasoning skills on optimization modeling. Our dataset is handcrafted by domain experts, i.e. OR experts, and is representative of different types of optimization and various application domains, such as vehicle routing, production planning, or investment portfolio allocation.

We contribute a novel multi-choice QA dataset for specialized technical domains. Each instance of the dataset contains the following:

1. An `input` context describing an optimization model as a case study.
2. A `question` asking about the understanding of the problem specifications (e.g. objective criterion or constraints), the underlying components of the corresponding optimization model (e.g. the elements participating in the optimization), as well as the structure and logic of the optimization model (e.g. the logical relation between two decision activities).
3. A list of `options` for the answer, which was handcrafted by OR experts to make the question challenging to guess. The LLM must select the correct answer from a list of four options.
4. The correct `target` answer.

It is important to emphasize that each question is designed to require basic knowledge of optimization, an understanding of the problem description, and, more importantly, multi-step reasoning. We have selected the field of operations research due to the high level of technical expertise required to understand and answer questions about optimization modeling.

We have carefully selected the optimization problems from various domains. Furthermore, each question/choice/answer instance has been curated and verified by domain experts. As a result, ORQA is positioned to be an impactful benchmark that can contribute to the evaluation of general-purpose LLMs' generalization ability on specialized domains and tasks.

## Motivation

Our proposed Operations Research Question Answering (ORQA) benchmark is highly relevant to the GenBench collaborative task, as it addresses the crucial aspect of generalization in natural language processing (NLP) models. Specifically focused on pretrained Large Language Models (LLMs) within the domain of Operations Research (OR), ORQA is designed to tackle the significant cross-domain shift issue. By presenting a multi-choice question answering task that tests reasoning skills and domain-specific knowledge in optimization modeling, ORQA provides a comprehensive evaluation platform.

As the first benchmark of its kind in Operations Research, ORQA serves as an open and collaborative platform to assess LLMs' real-world performance in specialized technical domains. The primary goal is to ensure responsible and well-informed deployment of LLMs, minimizing potential negative impacts. Notably, unlike technical reports from commercial LLM vendors, ORQA is an open-source benchmark, ensuring impartiality and transparency in the evaluation process. This approach aligns perfectly with our motivation to advance research on generalization in NLP and promote the responsible development of LLMs. By creating a benchmark that specifically targets optimization and Operations Research, we aim to foster a collective effort within the NLP community, enhancing the reliability and practical applicability of LLMs in professional domains.

## Examples

The motivation of the dataset is to test whether an LLM has reasoning abilities to answer questions about a mathematical model presented as a natural language problem description.

Here are two examples from the dataset. **More examples have been appended to the end of this file.**

**<u>EXAMPLE 1</u>**

**Context:**

As a supply chain manager for a leading cement manufacturing brand, you face a complex challenge. Your company manufactures two grades of cement from three different plants, each plant having distinct production capacities. To distribute these grades of cement, you have four distribution centers (DCs) at your disposal, each involving a fixed operating cost. Additionally, you serve five construction companies as customers, each requiring specific quantities of both cement grades. Your main objective is to minimize the total cost of transportation. This cost is split into two parts - the expense of transferring cement from a plant to a DC, and the cost of transporting the cement from a DC to a construction company. But remember, your ultimate goal is to satisfy all your construction customers' needs for both cement grades. Your challenge is to find the best way to distribute cement from the plants to the DCs, and then from the DCs to the construction companies. You need to respect the production capabilities of your plants and cater to the specific demands of your customers. Don't forget that every DC carries a fixed operating cost, and each has a status indicating whether it's in use or not. Your aim is to achieve the lowest total cost, encompassing both transportation and operational costs, while still meeting the demands of your construction customers. Cracking this problem is key. It lets you optimize your supply chain, lower expenses, and assure customer satisfaction by reliably meeting their cement needs. This is how you keep your brand competitive and responsive to market demand.

**Question:**

Which of the following elements define a set in the optimization model of the optimization problem?

**Target:**

3

**Target Options:**

0: Cement products

1: Plants and distribution centers

2: Construction companies, plants and distribution centers

3: Cement products, construction companies, plants and distribution centers

**<u>EXAMPLE 2</u>**

**Context:**

As the operations manager at Thunder Rail Co., your task is to manage a large railroad network that starts from the vibrant city of Metroville and ends at Terminus Town. This is not a simple two-point route; your network includes eight additional stations situated in various scenic and touristic locations facilitating the journey from Metroville to Terminus Town. The network comprises a total of ten stations, interconnected by several tracks. Each track has its own unique capacity, indicating the maximum number of trains it can accommodate simultaneously. Your primary goal is to optimize the flow of trains from Metroville to Terminus Town, ensuring no track is overloaded beyond its capacity. Keep in mind that each track has its own capacity, and not all can manage the same volume of train traffic. Your challenge lies in identifying the most efficient route distribution, maximizing the number of trains that can travel from Metroville to Terminus Town without surpassing any track's capacity.

**Question:**

Which of the following options defines a capacity constraint that is specified in the above problem description?

**Target:**

1

**Target Options:**

0: The number of passengers should not exceed the total capacity of the trains.

1: The number of trains running on a given track should not exceed the capacity of that track.

2: The number of passengers arriving at Terminus town should not exceed the number of passengers leaving at Metroville.

3: The number of trains leaving Metroville should be the same as the number of trains arriving at Terminus town.

Here, the **"Context"** field contains the natural language description of an optimization problem. This text comprehensively describes an optimization problem which can be formulated into an optimization model.

The **"Question"** field poses a modelling question related to the problem. These questions range from the classification of optimization model (optimization model type, problem category, etc.) to specific details of the optimization model (identification of constraints, relation between variables, element that a constraint is defined on, etc.).

The **"Target Options"** field presents the multiple choices and the "Target" field gives the correct option.

## Usage

The data is used for a Multiple-choice Question Answering task. The model is summarized as a problem description which is passed as `context` to a PLM. The `question` and list of four `target_options` are passed to the PLM and the PLM must choose <u>only</u> one answer from the passed `target_options`. The answer is then matched with the gold standard `target` field to determine the accuracy of the PLM when evaluated on this unseen test set from the highly-technical field of operations research.

## Data Source

Our dataset was generated through a three-step process executed by Operations Research (OR) experts. First, over 200 optimization problems were selected from various open-source resources across 15 application domains, ensuring balanced representation, real-world relevance, and medium complexity. Each problem included a natural language description and an optimization model. Subsequently, the experts designed 12 unique question types, each intentionally crafted to necessitate multi-step reasoning.

In the second step, the experts refined questions, created four options, and selected the target answer for each question type and optimization problem pair, creating instances with a context, question, four options, and a target answer. This yielded over 2200 multiple-choice questions and answers.

Lastly, a dual-stage verification process was conducted by two OR experts for each instance. This process focused on verifying completeness, clarity, correctness of the target answer, and the necessity of multi-step reasoning, ensuring the reliability of our dataset. The data creation process is graphically described in this [figure](Data_creation.png).

## Limitations and Bias

Any decision-making problem may be formulated as an optimization model. Thus, the field of OR spans all domains and it is infeasible for our dataset to comprehensively represent all domains. This benchmark is limited by the coverage of domains as it targets more common domains of OR.

## GenBench Eval card

The [GenBench Evaluation Card](OpResearchQA-EvalCard.PNG) describes the type of generalization that ORQA is evaluating.

**GenBench Taxonomy Values:**

- _Motivation_: Practical. Operations research is applied in many industries with various applications.
- _Generalisation type_: Cross-domain. We understand that LLMs are pretrained on a large and diverse set of Corpora. However, we believe the corpora of specialized domains such as Operations Research is very scarce on the open web and it difficult to access. Therefore, it is more difficult for LLMs to generalize to this specific target domain.
- _Shift type_: Covariate. For multi-choice QA task, we were not sure how the label shift plays a role in our setting. Therefore, we have selected covariate shift as the type in our taxonomy.
- _Shift source_: Naturally occurring. The descriptions of the optimization problems were hand-written and edited by domain experts.
- _Shift locus_: Pretrain-test. We focus on testing the ability of Pretrained Language models without fine-tuning. This is motivated by the expensive cost of building large-scale dataset and but this choice is also by design since we want to verify the real capabilities of LLMs on zero-shot or few-shot settings.

## Additional Examples

Each of the below **Questions** would be combined with the **Context** in the 'input'. However, for the sake of space, we are displaying the **Context** once:

**Context**

As a manager in a well-established fashion retail company, you're faced with a critical responsibility: deciding what products to feature in your store. Your customers, segmented into various groups based on preferences and shopping behavior, have clearly defined tastes. Your role is to cater to these tastes while considering the profitability of each product and the costs associated with stocking them. Each customer segment represents a unique buying capacity, akin to a maximum sales volume per group. Within each segment, customers have a distinct preference order for different clothing items. When they shop, they will opt for their top preferred item available, but only if their preference level for that item is above zero. In your arsenal, you have a catalog of potential items to sell. Each item comes with a specific profit margin and a fixed stocking cost. Additionally, you have data about each customer segment's preference for each product. Your task is to curate an optimized product mix that maximizes your total profit. This involves considering both the profit per item sold and the fixed cost of stocking each item. By skillfully navigating this task and selecting the right array of products, you can strike a balance between increasing profits and ensuring customer satisfaction. Furthermore, this insight into your customer segments and their preferences will enhance your merchandising strategies, aiding in better targeted marketing campaigns and an overall improved business strategy.

**Question**

Which of the following logical relations is incorrect regarding the customer buying behavior and their preferences?

**Target:**

2

**Target Options:**

0: A customer will not buy a fashion item if a more preferred product is offered for its customer segment.

1: A customer segment will not buy an item if its preference for that item is zero.

2: A customer in a given segment will always buy its most preferred fashion item.

3: Each customer segment buys at most one fashion item.

**Question**

Which of the following elements define a set that is needed to formulate an optimization model for this problem?

**Target:**

1

**Target Options:**

0: Products and Customers

1: Products and Segments

2: Customers and Groups

3: Products, Customers, and Groups

**Question**

Which of the following constraint should also be required to properly formulate the optimization problem?

**Target:**

0

**Target Options:**

0: Each customer segment should be assigned to buy at most one type of product.

1: Each customer segment should be assigned to buy one and only one type of product.

2: Each customer segment should buy its most preferred product.

3: Each customer segment should buy its most preferred product or another most preferred product by the other segments.

For more details, our data samples can be accessed through the `data_source` field within `config.jsonnet` or [GitHub - OpResearchQA/ORQA_data: Dataset for the ORQA benchmark](https://github.com/OpResearchQA/ORQA_data/tree/main).  This specific context has 9 questions associated with it. 
