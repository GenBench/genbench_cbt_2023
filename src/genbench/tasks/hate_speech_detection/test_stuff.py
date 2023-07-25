from genbench import load_task
from genbench.api import PreparationStrategy

task = load_task("hate_speech_detection")
ds = task.get_prepared_datasets(
    PreparationStrategy.PROMPT_BASED_TESTING, 
    shot_list=[0]
)[0]
print(ds[0])
# {
#   'input': 'Add two numbers together\n\nQ: 300 + 80\nA: ', 
#   'target': '380', 
#   '_genbench_idx': 0, 
#   ...
#  }