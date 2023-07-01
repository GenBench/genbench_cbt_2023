from genbench import Task


class MyAwesomeTaskDictSubtask1(Task):
    def format_example(self, example):
        return {
            "input": f"{example['input']} hello inn11!",
            "target": f"{example['target']} hello out11!",
        }
