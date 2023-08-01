# Train-test data splits of the Europarl NMT corpus with divergent distributions of dependency relations
## Abstract
To assess NMT models' capacity to translate novel syntactical structures, we split the Europarl parallel corpus into training and testing sets with divergent distributions of the syntactical structures. We derive the data splitting method from the *distribution-based compositionality assessment* (DBCA) method introduced by Keysers et al. (2020). We define the *atoms* as the lemmas and dependency relations, and the *compounds* as the three-element tuples of two lemmas (the head and the dependant), and their relation, for instance `(appreciate, dobj, vigilance)`. 


## Examples
The task is simply sentence-level translation, e.g.:
```
"input": "If the House agrees, I shall do as Mr Evans has suggested.", "target": "Jos parlamentin jäsenet kannattavat sitä, teen niin kuin jäsen Evans ehdotti."
```


## Usage
To use the provided train-test split, load the data from
```
# Load the task
task = load_task("dbca_deprel")
ds = task.get_prepared_datasets(PreparationStrategy.FINETUNING)

# Load model predictions and evaluate
preds = ...
print(task.evaluate_predictions(
            predictions=preds,
            gold=ds,
        )
    )
```

To compute the atom and compound divergences for any pair of training (pre-training, training and/or fine-tuning) and test data sets, use the script `calculate_divergences.py`. To create the atom and compound distributions of the two sets, the frequencies of each atom and compound in each set need to be calculated first. 

## Data Source
The original data source is `https://www.statmt.org/europarl/`

## Limitations and Bias
*Note any known limitations or biases that the dbca_deprel has, with links and references if possible.*

## GenBench Eval card
![GenBench Eval Card](eval_card.png)
