import dataclass_factory
from task import NlCodesearchMrrCodesearchnetAdv

from genbench.task_config import TaskConfig
from genbench.utils.file import load_jsonnet


def main():
    high_mrr_test_list = []
    for i in range(1, 11):
        score_dict = dict.fromkeys(["score"])
        score_dict["score"] = 1 / i
        high_mrr_test_list.append(score_dict)

    low_mrr_test_list = []
    for i in range(1, 11):
        score_dict = dict.fromkeys(["score"])
        score_dict["score"] = 1 * i
        low_mrr_test_list.append(score_dict)

    cfg_file = load_jsonnet("./config.jsonnet")
    factory = dataclass_factory.Factory()
    config: TaskConfig = factory.load(cfg_file, TaskConfig)

    task = NlCodesearchMrrCodesearchnetAdv(config, "nl_codesearch_mrr")
    output_ds = task.get_dataset_raw(9)

    high_results = task.evaluate_predictions(high_mrr_test_list, output_ds, 9)
    print(high_results)

    low_results = task.evaluate_predictions(low_mrr_test_list, output_ds, 9)
    print(low_results)


if __name__ == "__main__":
    main()
