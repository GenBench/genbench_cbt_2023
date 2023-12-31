import numpy as np
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForMaskedLM,
    AutoTokenizer,
    MT5ForConditionalGeneration,
    T5ForConditionalGeneration,
    XGLMTokenizer,
)

from genbench import load_task
from genbench.api import PreparationStrategy


# No need for changing this function
# This function calculates the probabilities of each candidate
def predict_mask(answer_cand, prompt, mname, lang):
    answer_pred_probs = dict()

    for answer in answer_cand:
        answer_cand_probs = []

        if (
            "t5" not in mname
            and "xglm" not in mname
            and "opt" not in mname
            and "bloom" not in mname
            and "llama" not in mname
            and "gpt" not in mname
        ):
            answer_tokens = tokenizer(answer)["input_ids"][1:-1]

            if "xlm-roberta" in mname and answer_tokens[0] == 6 and lang == "zh":
                answer_tokens = answer_tokens[1:]

            new_mask = ["<mask>"] * len(answer_tokens)

            if lang == "zh":
                new_mask = "".join(new_mask)
            else:
                new_mask = " ".join(new_mask)

            prompt_new = prompt.replace("<mask>", new_mask)
            prompt_new = prompt_new.replace("<mask>", tokenizer.mask_token)

            for j, w_idx in enumerate(answer_tokens):
                model_inputs = tokenizer(prompt_new, return_tensors="pt").to(device)
                model_outputs = model(**model_inputs)
                input_ids = model_inputs["input_ids"][0]
                outputs = model_outputs["logits"]
                masked_index = torch.nonzero(input_ids == tokenizer.mask_token_id, as_tuple=False)

                logits = outputs[0, masked_index[0].item(), :]
                probs = logits.softmax(dim=-1).detach().cpu().numpy()
                answer_cand_probs.append(-np.log(probs[w_idx]))

                pos = prompt_new.find(tokenizer.mask_token)
                prompt_new = (
                    prompt_new[:pos]
                    + tokenizer.convert_ids_to_tokens(w_idx)
                    + prompt_new[pos + len(tokenizer.mask_token) :]
                )

            answer_pred_probs[answer] = np.mean(answer_cand_probs)

        elif "xglm" in mname or "opt" in mname or "bloom" in mname or "llama" in mname or "gpt" in mname:
            prompt_new = prompt.replace("<mask>", answer)

            model_input = tokenizer(prompt_new, return_tensors="pt").to(device)
            output = model(**model_input)

            if lang == "zh":
                logits = output["logits"][0, :-1]
                token_ids = model_input["input_ids"][0, 1:]
            else:
                logits = output["logits"][0, :-2]
                token_ids = model_input["input_ids"][0, 1:-1]

            answer_pred_probs[answer] = float(torch.nn.CrossEntropyLoss(reduction="mean")(logits, token_ids))
        else:
            input_ids = tokenizer(prompt.replace("<mask>", "<extra_id_0>"), return_tensors="pt").input_ids.to(device)
            labels = tokenizer("<extra_id_0> " + answer + " <extra_id_1>", return_tensors="pt").input_ids.to(device)
            target_ids = labels[0][1:-2]

            outputs = model(input_ids=input_ids, labels=labels).logits
            masked_index = torch.tensor(list(range(outputs.size()[1]))[1:-2])

            for idx, t_idx in zip(masked_index, target_ids):
                logits = outputs[0, idx.item(), :]
                probs = logits.softmax(dim=-1).detach().cpu().numpy()
                answer_cand_probs.append(-np.log(probs[t_idx]))

            answer_pred_probs[answer] = np.mean(answer_cand_probs)

    return answer_pred_probs


cross_ling_const_task = load_task("cross_lingual_consistency")

# Variables (Input dataset, langs and model)
mini = True  # True for BMLAMA-17; False for BMLAMA-53
lang1 = "en"
lang2 = "es"
mname = "bigscience/bloom-3b"

# Setup dataset
# The dataset length is num_languages * num_instances_per_language
ds = cross_ling_const_task.get_prepared_datasets(
    preparation_strategy=PreparationStrategy.PROMPT_BASED_TESTING,
    mini=mini,
    lang1=lang1,
    lang2=lang2,
)


# Setup model & tokenizer
if "xglm" in mname or "opt" in mname or "bloom" in mname or "llama" in mname or "gpt" in mname:
    model = AutoModelForCausalLM.from_pretrained(mname)
elif "google/mt5" in mname:
    model = MT5ForConditionalGeneration.from_pretrained(mname)
elif "t5" in mname:
    model = T5ForConditionalGeneration.from_pretrained(mname)
else:
    model = AutoModelForMaskedLM.from_pretrained(mname)

if "xglm" in mname:
    tokenizer = XGLMTokenizer.from_pretrained(mname)
else:
    tokenizer = AutoTokenizer.from_pretrained(mname)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("Runing on:" + device)
print()
model = model.to(device)

# Store the ranked candidates
ranked_keys_list = []
# Store the original candidates
origin_keys_list = []

# Reranking based on prob
for i, data in enumerate(ds):
    # The form of each data:
    # {
    #   "input": "The capital of Canada ",
    #   "target": "Ottawa",
    #   "target_options": [
    #       "Beijing",
    #       "Tokyo",
    #       "Ottawa",
    #   ],
    #   "_genbnech_idx": <some index>
    # }

    logprobs = []
    lang = lang1 if i < len(ds) / 2 else lang2

    answer_pred_probs = predict_mask(data["target_options"], data["input"], mname, lang)
    origin_keys_list.append(answer_pred_probs)

    sorted_probs = sorted(answer_pred_probs.items(), key=lambda x: x[1], reverse=False)
    ranked_keys = [x[0] for x in sorted_probs]
    ranked_keys_list.append(ranked_keys)

# Evaluate Cross Lingual Consistency:
results = cross_ling_const_task.evaluate_predictions(ranked_keys_list, origin_keys_list)
print(results)
