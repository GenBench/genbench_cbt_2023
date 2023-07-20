from genbench import load_task
from genbench.api import PreparationStrategy

from transformers import AutoModelForCausalLM
from transformers import pipeline

from tqdm import tqdm

n_datapoints = 2

task = load_task("icl_consistency_test")
ds = task.get_prepared_datasets(PreparationStrategy.PROMPT_BASED_TESTING, shot_list=[0])[0]

# selecting a subset of example for illustration purposes
subset = list(set(ds['data_ID']))[:n_datapoints]
ds = ds.filter(lambda x: x['data_ID'] in subset)

generator = pipeline('text-generation', model='DistilGPT2')

predictions = {}
for datapoint in tqdm(ds):
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

results = task.evaluate_predictions(predictions=predictions, gold=ds)
