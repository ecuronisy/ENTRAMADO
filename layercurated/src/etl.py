import importlib.util
import json
import os

def load_pipeline_config(file_path):
    """
    Loads the pipeline configuration from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the pipeline configuration.

    Returns:
        dict: A dictionary representing the pipeline configuration loaded from the file.
    """

    with open(file_path, 'r') as file:
        return json.load(file)


def execute_task(task_path, base_parameters):
    """
    Executes a task by loading its script from a file and executing it with the given base parameters.

    Args:
        task_path (str): The path to the script file containing the task.
        base_parameters (dict): A dictionary containing the base parameters to be injected into the task's execution context.
    """

    spec = importlib.util.spec_from_file_location("module.name", task_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.run(base_parameters)


def run_pipeline(pipelines_file_path):
    """
    Runs all pipelines by loading its configuration and executing its tasks.

    Args:
        pipelines_file_path (str): The path to the JSON file containing the pipelines configuration.
    """

    pipelines = load_pipeline_config(pipelines_file_path)
    
    for pipeline in pipelines['pipelines']:
        print(f"Running pipeline {pipeline['name']}")
        for task in pipeline['tasks']:
            task_path = task['task']['task_path']
            base_parameters = task['task']['base_parameters']
            print(f"Executing task {task['task_key']} in pipeline {pipeline['name']}")
            execute_task(task_path, base_parameters)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pipelines_file_path = os.path.join(script_dir, "pipelines.json")
    
    try:
        run_pipeline(pipelines_file_path)
    except Exception as e:
        print(f"Error: {e}")