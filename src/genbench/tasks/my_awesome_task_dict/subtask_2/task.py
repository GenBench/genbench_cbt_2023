from genbench import Task


class MyAwesomeTaskDictSubtask2(Task):
    def format_example(self, example):
        return {
            "input": f"{example['input']} hello inn222!",
            "target": f"{example['target']} hello out222!",
        }
