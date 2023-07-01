from genbench import Task


class MyAwesomeTaskTask(Task):
    def format_example(self, example):
        return {
        	"input": f"{example['input']} hello inn!",
        	"target": f"{example['target']} hello out!",
        }
