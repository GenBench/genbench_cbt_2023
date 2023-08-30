"""
EXAMPLE USAGE OF ICL CONSISTENCY TEST

This script requires additional packages to be installed:

pip install torch
pip install git+https://github.com/huggingface/transformers.git
pip install bitsandbytes
pip install accelerate

"""
import string
from typing import Dict, List

import torch
import transformers
from torch import Tensor
from torch.utils.data import DataLoader
from tqdm import tqdm

from genbench import load_task
from genbench.api import PreparationStrategy


N_DATAPOINTS = 50
MODEL_NAME = "huggyllama/llama-7b"
BATCH_SIZE = 8

device = "cuda" if torch.cuda.is_available() else "cpu"


class Generator:
    """
    A simple wrapper to evaluate a given hf-model
    """
    def __init__(self, model_name="huggyllama/llama-7b"):
        self.max_new_tokens = 4  # some labels consist of up to 4 tokens
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            model_name,
            device_map="auto",
            padding_side="left",
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True,
            device_map="auto",
        ).eval()

        self.generation_config = transformers.GenerationConfig(
            do_sample=False,
            return_dict_in_generate=False,
            output_scores=True,
            max_new_tokens=self.max_new_tokens,
            return_full_text=False,
        )

    def generate(self, prompt) -> List[str]:
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)

        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        generation_output = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            generation_config=self.generation_config,
        )

        outputs = self.tokenizer.batch_decode(generation_output[:, input_ids.shape[1] :])

        # do some post-processing
        outputs = [o.strip().split()[0].translate(str.maketrans("", "", string.punctuation)) for o in outputs]

        return outputs

    def make_predictions(self, dataset, bs=8) -> Dict[str, Dict[str, str]]:
        out = {}
        dl = DataLoader(dataset=dataset, batch_size=bs, num_workers=0)

        with torch.no_grad():
            for batch in tqdm(dl):
                prediction = self.generate(batch["input"])

                # organize predictions into output dictionary
                for i, (data_ID, setup_ID) in enumerate(zip(batch["data_ID"], batch["setup_ID"])):
                    data_ID = str(data_ID.item() if isinstance(data_ID, Tensor) else data_ID)
                    if setup_ID in out.keys():
                        out[setup_ID].update({data_ID: prediction[i]})
                    else:
                        out[setup_ID] = {data_ID: prediction[i]}

        return out


if __name__ == "__main__":
    # Load the task
    task = load_task("icl_consistency_test")
    ds = task.get_prepared_datasets(PreparationStrategy.PROMPT_BASED_TESTING, shot_list=[0])[0]

    # Selecting a subset of example for illustration purposes
    subset = list(set(ds["data_ID"]))[:N_DATAPOINTS]
    ds = ds.filter(lambda x: x["data_ID"] in subset)

    # Generate predictions for the dataset
    generator = Generator(model_name=MODEL_NAME)
    predictions = generator.make_predictions(ds, bs=BATCH_SIZE)

    # OPTIONAL: The ICL-consistency test provides the option to add factors to the analysis by using the
    # `add_factor` method.
    add_external_factor = False
    if add_external_factor:
        predictions_external_factor = ...  # some function generating alternative predictions
        predictions = task.add_factor(data=(predictions, predictions_external_factor), factor="<my-external-factor>")

    # Evaluate the predictions
    results = task.evaluate_predictions(predictions=predictions, gold=ds)

    print("EVALUATED SUCCESSFULLY!")
    print(f'Exact-match accuracies: \n{results["exact_match_accuracy"]["accuracy"]}')
    print(f'Consistency: \n{results["kappas"]}')
