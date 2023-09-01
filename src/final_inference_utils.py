import sys


def get_folder_path(experiment_name):
    return sys.path[0] + "/output_of_llms/" + experiment_name
