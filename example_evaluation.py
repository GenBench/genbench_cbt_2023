from genbench import load_task
from genbench.api import PreparationStrategy

from transformers import AutoModelForCausalLM
from transformers import pipeline

from tqdm import tqdm

# delete after testing
import torch
import os

N_DATAPOINTS = 1


def make_predictions(generator, dataset):
    predictions = {}
    for datapoint in tqdm(dataset):
        prediction = generator(datapoint['input'],
                               max_new_tokens=1,
                               num_return_sequences=1,
                               do_sample=False,
                               return_full_text=False,
                               pad_token_id=generator.tokenizer.eos_token_id
                               )
        current_setup = str(datapoint['setup_ID'])
        current_data_ID = str(datapoint['data_ID'])

        if current_setup in predictions.keys():
            predictions[current_setup].update({current_data_ID: prediction[0]['generated_text'].strip()})
        else:
            predictions[current_setup] = {current_data_ID: prediction[0]['generated_text'].strip()}

    return predictions


if __name__ == '__main__':
    # Load the task
    task = load_task("icl_consistency_test")

    if not os.path.exists(f'cache_{N_DATAPOINTS}.p'):
        ds = task.get_prepared_datasets(PreparationStrategy.PROMPT_BASED_TESTING, shot_list=[0])[0]

        # Selecting a subset of example for illustration purposes
        subset = list(set(ds['data_ID']))[:N_DATAPOINTS]
        ds = ds.filter(lambda x: x['data_ID'] in subset)

        # Generate predictions for the dataset
        generator = pipeline('text-generation', model='gpt2')
        predictions = make_predictions(generator, ds)

        # OPTIONAL: The ICL-consistency test provides the option to add factors to the analysis by using the
        # `add_factor` method (here exemplified with distillation).
        generator_distil = pipeline('text-generation', model='DistilGPT2')
        predictions_distil = make_predictions(generator_distil, ds)
        torch.save((predictions, predictions_distil, ds), f'cache_{N_DATAPOINTS}.p')
    else:
        predictions, predictions_distil, ds = torch.load(f'cache_{N_DATAPOINTS}.p')
    predictions = task.add_factor(data=(predictions, predictions_distil), factor='distillation')
    # Evaluate the predictions
    results = task.evaluate_predictions(predictions=predictions, gold=ds)

    print('EVALUATED SUCCESSFULLY!')
    print(f'Exact-match accuracies: \n{results["exact_match_accuracy"]}')
    print(f'Consistency: \n{results["kappas"]}')
