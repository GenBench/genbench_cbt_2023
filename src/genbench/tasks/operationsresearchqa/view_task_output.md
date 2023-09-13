## 

## Results from "viewing our task"

Running the following code:

```
from genbench import load_task
from genbench.api import PreparationStrategy

task = load_task("operationsresearchqa:standard")
ds = task.get_prepared_datasets(
    PreparationStrategy.PROMPT_BASED_TESTING,
    shot_list=[0]
)[0]
print(ds[0])
```

```
{'id': '64c9580157a0b0ff5c8f196b', 
 'context': "As a finance manager in charge of a pension fund, your challenge is to build a portfolio that minimizes downside risk, using an array of assets such as stocks, bonds, or other financial instruments. To guide your strategy, you use historical returns data from these assets. Importantly, you must work within an eight-figure budget constraint, ensuring the total investment across all assets meets your target return.\nDownside risk refers to the potential loss if investment returns fall short of a pre-set acceptable level. You quantify this risk using a quadratic power function (power of 2). When this level aligns with your target return, you assess the downside risk as the semi-variance, a standard practice in finance for evaluating investment risk.\nThe historical returns data for each asset under different market conditions is a valuable resource to anticipate potential downside risks. With this information at your disposal, you can determine the optimal allocation of your investments among different financial instruments. As a result, you're able to meet your goal of creating a pension fund portfolio that satisfies your target return while keeping downside risk to a minimum, ensuring long-term growth and stability for the fund.", 
 'question': 'In the optimization model for this problem, which of the below parameters is used to define  the objective function?', 
 'target_options': ['The desired return', 'The threshold for acceptable return', 'The exponent two used in the power function for risk calculation', 'The possible scenarios from the historical dataset'], 
 'target': 'The exponent two used in the power function for risk calculation', 
 'input': "Given the context (following Context:), select the most appropriate answer to the question (following Question:)\n\nContext: As a finance manager in charge of a pension fund, your challenge is to build a portfolio that minimizes downside risk, using an array of assets such as stocks, bonds, or other financial instruments. To guide your strategy, you use historical returns data from these assets. Importantly, you must work within an eight-figure budget constraint, ensuring the total investment across all assets meets your target return.\nDownside risk refers to the potential loss if investment returns fall short of a pre-set acceptable level. You quantify this risk using a quadratic power function (power of 2). When this level aligns with your target return, you assess the downside risk as the semi-variance, a standard practice in finance for evaluating investment risk.\nThe historical returns data for each asset under different market conditions is a valuable resource to anticipate potential downside risks. With this information at your disposal, you can determine the optimal allocation of your investments among different financial instruments. As a result, you're able to meet your goal of creating a pension fund portfolio that satisfies your target return while keeping downside risk to a minimum, ensuring long-term growth and stability for the fund.\nQuestion: In the optimization model for this problem, which of the below parameters is used to define  the objective function?\nChoices:\nThe desired return\nThe threshold for acceptable return\nThe exponent two used in the power function for risk calculation\nThe possible scenarios from the historical dataset\nAnswer: ", 
 '_genbench_idx': 0, 
 'original_input': "\nContext: As a finance manager in charge of a pension fund, your challenge is to build a portfolio that minimizes downside risk, using an array of assets such as stocks, bonds, or other financial instruments. To guide your strategy, you use historical returns data from these assets. Importantly, you must work within an eight-figure budget constraint, ensuring the total investment across all assets meets your target return.\nDownside risk refers to the potential loss if investment returns fall short of a pre-set acceptable level. You quantify this risk using a quadratic power function (power of 2). When this level aligns with your target return, you assess the downside risk as the semi-variance, a standard practice in finance for evaluating investment risk.\nThe historical returns data for each asset under different market conditions is a valuable resource to anticipate potential downside risks. With this information at your disposal, you can determine the optimal allocation of your investments among different financial instruments. As a result, you're able to meet your goal of creating a pension fund portfolio that satisfies your target return while keeping downside risk to a minimum, ensuring long-term growth and stability for the fund.\nQuestion: In the optimization model for this problem, which of the below parameters is used to define  the objective function?\nChoices:\nThe desired return\nThe threshold for acceptable return\nThe exponent two used in the power function for risk calculation\nThe possible scenarios from the historical dataset",
 'original_target': 2}
```
