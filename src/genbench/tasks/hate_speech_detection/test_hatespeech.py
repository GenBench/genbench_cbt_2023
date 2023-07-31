from genbench import load_task
from genbench.api import PreparationStrategy


task = load_task("hate_speech_detection")
ds = task.get_prepared_datasets(PreparationStrategy.FINETUNING)
print(ds)
print(ds["test"][0])


# {
#   'input': 'Add two numbers together\n\nQ: 300 + 80\nA: ',
#   'target': '380',
#   '_genbench_idx': 0,
#   ...
#  }
