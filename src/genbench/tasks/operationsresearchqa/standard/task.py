from typing import Any, Dict

from genbench import Task


def idx_to_ltr(idx):
    return chr(int(idx) + ord("A"))


class OperationsresearchqaStandard(Task):
    def format_example(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform preprocessing/formatting on an example-level.
        Args:
            example: A dictionary containing key-value pairs for an example from the source dataset.
        Returns:
            A dictionary containing key-value pairs for the preprocessed/formatted example.
            The dictionary should contain keys `input` and `target`.
        """
        input_str = self.get_input_string(example)
        target_str = str(idx_to_ltr(example["target"]))
        print(target_str)

        return {
            "input": input_str,
            "target": target_str,
        }

    def get_input_string(self, example: Dict[str, Any]):
        """
        A zero-shot example:
        Given the context (following Context:), select the most appropriate answer
        to the question (following Question:). Answer only 'A', 'B', 'C', or 'D'.
        Context: As a manager in an advertising agency, we are currently facing a media selection
        problem for one of our clients. Our client wants to place ads in various media
        to reach different demographic groups. Based on viewing and readership
        data, we have a table that shows the number of exposures obtained in each market
        segment per dollar spent on advertising in each medium. For each market segment,
          we have decided on a minimum desired number of exposures, as we believe
        that we must reach at least this number of readers or viewers, regardless of the cost. We also have a
        saturation level, which indicates that any exposure beyond this level is of no value to our client.
        Exposures between these two limits are considered useful exposures. Our objective is to determine how
        much should be spent on advertising in each medium, given an advertising budget and a target minimum of
        total useful exposures over all markets. The available media options include late-night TV, prime time TV,
        newspapers, billboards, and radio. We aim to maximize the overall impact of our client's advertising
        campaign while staying within budget and achieving the target minimum total useful exposures.
        Question: Which data parameters are participating in the objective criterion for this problem?
        A. Number of exposures achieved in a specific market segment per dollar spent on a specific media
        B. Total number of exposures achieved in each market segment
        C. Amount of money to be spent on advertising in each media channel
        D. None of the above
        Answer:

        """

        context_NL = example["context"]
        question_NL = example["question"]
        option_0 = example["target_options"][0]
        option_1 = example["target_options"][1]
        option_2 = example["target_options"][2]
        option_3 = example["target_options"][3]

        input_str = (
            "Context: "
            + str(context_NL)
            + "\nQuestion: "
            + str(question_NL)
            + "\nA. "
            + str(option_0)
            + "\nB. "
            + str(option_1)
            + "\nC. "
            + str(option_2)
            + "\nD. "
            + str(option_3)
        )

        return input_str
