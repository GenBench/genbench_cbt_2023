## Motivation
It is widely acknowledged that fine-tuning a pretrained model generally results in better performance on a given task, compared to training the model from scratch. Evidence suggest that this is also the case for compositional generalization tasks. However, it has also been shown that multilingual models may not exhibit consistent performance across languages, with low resource languages often doing worse. Can we expect similar variations between languages when testing a multilingual model for compositionality?

The majority of research on compositional generalisation has focussed on English data and models. With the ambition to gain a deeper understanding on this issue from a multilingual perspective, we aim to adapt SCAN an existing compositionality benchmark into multiple languages, in order to evaluate multilingual LLMs for compositional generalization. 


## Examples
We have five subtasks, corresponding each to five languages: French (fra), Hindi (hin), Russian (ru), Turkish (tur), and Mandarin Chinese (cmn). 

Each subtasks consists of the adapted SCAN dataset into the aforementioned languages. 

Example: 

ENG-SCAN

IN: walk opposite right thrice after run opposite right 
OUT: I_TURN_RIGHT I_TURN_RIGHT I_RUN I_TURN_RIGHT I_TURN_RIGHT I_WALK I_TURN_RIGHT I_TURN_RIGHT I_WALK I_TURN_RIGHT I_TURN_RIGHT I_WALK


FRA-SCAN 
IN: marcher à l'envers par la droite trois fois après courir à l'envers par la droite 
OUT: I_TURN_RIGHT I_TURN_RIGHT I_RUN I_TURN_RIGHT I_TURN_RIGHT I_WALK I_TURN_RIGHT I_TURN_RIGHT I_WALK I_TURN_RIGHT I_TURN_RIGHT I_WALK

## Data Source
To generate the data, native speakers of the five selected languages have been asked to manually translate the vocabulary of the original SCAN dataset as well as either the equivalent interpretation function or grammar in their own language. 

## Limitations and Bias
*Note any known limitations or biases that the Multilingual SCAN has, with links and references if possible.*

## Citation
**
## Further References
Original SCAN benchmark paper (Lake & Baroni, 2018): https://arxiv.org/abs/1711.00350
