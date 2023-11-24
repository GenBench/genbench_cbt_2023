from genbench import load_task


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

    task = load_task("nl_codesearch_mrr:statcodesearch")

    high_results = task.evaluate_predictions(high_mrr_test_list, 9)
    print(high_results)

    low_results = task.evaluate_predictions(low_mrr_test_list, 9)
    print(low_results)


if __name__ == "__main__":
    main()
