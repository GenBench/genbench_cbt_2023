# Cross-lingual Local QA

## Abstract
Given the large presence of local knowledge in popular QA datasets (e.g., TriviaQA) that predominantly probe for Anglo-specific knowledge, our Cross-lingual Local Question Answering (QA) task is specifically designed to measure the presence of local and culture-specific knowledge in Large Language Models (LLMs), as well as its generalisation across languages. For this purpose, a hand-crafted dataset was created, containing question templates locally adapted to seven different localities: Ethiopia, The Netherlands, UK, Germany, India, Mexico, and Spain. These questions were then translated into the corresponding languages: 'am-ET', 'nl-NL', 'en-GB', 'de-DE', 'hi-IN', 'es-MX', 'es-ES', resulting in 49 QA pairs per general template. The effort extends beyond the traditional Anglo-centric focus, aiming to offer a broader and more inclusive examination of LLMs' ability to handle localised information from various cultural contexts.


## Example
'''
{
    "2": {
        "category": "geography",
        "template": "In which {country} city would you find {landmark}?",
        "localities": {
            "Ethiopia": [
                {
                    "question_template": "In which {Ethiopian} city would you find {Lalibela Church}?",
                    "answer_template": "Lalibela",
                    "translations": {
                        "am-ET": {
                            "question": "ላሊበላ ቤተክርስትያን በየትኛው ከተማ ይገኛል?",
                            "answer": "ላሊበላ"
                        },
                        "nl-NL": {
                            "question": "In welke Ethiopische stad staat de Lalibela-kerk?",
                            "answer": "Lalibela"
                        },
                        "en-GB": {
                            "question": "In which Ethiopian city would you find Lalibela Church?",
                            "answer": "Lalibela"
                        },
                        "de-DE": {
                            "question": "In welcher äthiopischen Stadt befindet sich die Lalibela-Kirche?",
                            "answer": "Lalibela"
                        },
                        "hi-IN": {
                            "question": "आपको इथियोपिया के किस शहर में लालिबेला चर्च मिलेगा?",
                            "answer": "लालिबेला"
                        },
                        "es-MX": {
                            "question": "¿En qué ciudad etiope se encuentran las iglesias en la roca de Lalibela?",
                            "answer": "Lalibela"
                        },
                        "es-ES": {
                            "question": "¿En qué ciudad etiope se encuentra la escultura conocida como las iglesias en la roca de Lalibela?",
                            "answer": "Lalibela"
                        }
                    }
                }
            ],
            "Netherlands": [
                {
                    "question_template": "In which {Dutch} city would you find {Euromast}?",
                    "answer_template": "Rotterdam",
                    "translations": {
                        "am-ET": {
                            "question": "በየትኛው የኔዘርላንድ ከተማ ዩሮማስትን ያገኛሉ?",
                            "answer": "ሮተርዳም"
                        },
                        "nl-NL": {
                            "question": "In welke Nederlandse stad staat de Euromast?",
                            "answer": "Rotterdam"
                            [...]
'''


## Data Source
Hand-crafted QA data set by native speakers.


