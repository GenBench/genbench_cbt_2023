# Latent feature based Data Split (bert_closest_split)

## Abstract
This project aims to go beyond the random train-test split by developing a more challenging data-splitting process 
to better evaluate generalisation performance.
We rely on a models internal representations to create a data split and create the split by clustering the internal representations and assigning clusters to either the train or the test set.
Hate Speech is used as a testing ground for developing the splitting method.

## Examples
{"input": "wow do not all speak at once niggers", "target": 0, "target_options": ["hate", "noHate", "offensive"]}  
{"input": "how long will jews be a majority in israel", "target": 1, "target_options": ["hate", "noHate", "offensive"]} 
{"input": "sounds like something a moslem would do", "target": 2, "target_options": ["hate", "noHate", "offensive"]}

## Usage
For the task, the model has to decide whether a social media post includes hate speech, offensive speech or normal sentences.

## Data Source
The dataset was published in `HateXplain: A Benchmark Dataset for Explainable Hate Speech Detection ` by  Binny Mathew, Punyajoy Saha,
Seid Muhie Yimam, Chris Biemann, Pawan Goyal and Animesh Mukherjee in 2021. It was accepted at AAAI 2021.

It is licensed under the MIT License:

Copyright (c) 2020 Punyajoy Saha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Limitations and Bias
*Note any known limitations or biases that the Hate Speech Detection has, with links and references if possible.*

## GenBench Eval card
This method can be used to test generalisation in HateSpeech for LLMs (pretrain - test locus).
The split is based on the feature representations of a language model, therefore we assume that the shift is a covariate 
shift. The method assesses the robustness of language models and how well they generalise.
![GenBench Eval Card](eval_card.png)
