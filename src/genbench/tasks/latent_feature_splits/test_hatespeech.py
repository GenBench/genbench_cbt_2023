from genbench import load_task
from genbench.api import PreparationStrategy


task = load_task("latent_feature_splits:bert_closest_split")
ds = task.get_prepared_datasets(PreparationStrategy.FINETUNING)
print(ds)
print(ds["test"][0])
