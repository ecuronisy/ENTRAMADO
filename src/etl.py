import importlib.util
import json
import os
import sys


def load_pipeline_config(file_path):

    """
    Loads the pipeline configuration from a JSON file.

    :param file_path: The path to the JSON file containing the pipeline configuration.
    :return: A dictionary representing the pipeline configuration loaded from the file.
    """

    with open(file_path, 'r') as file:
        return json.load(file)


def execute_task(task_path, base_parameters):

    """
    Executes a task by loading its script from a file and executing it with the given base parameters.

    :param task_path: The path to the script file containing the task.
    :param base_parameters: A dictionary containing the base parameters to be injected into the task's execution context.
    :return: None
    """

    spec = importlib.util.spec_from_file_location("module.name", task_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.run(base_parameters)


def run_pipeline(pipeline_name, pipelines_file_path):

    """
    Runs a specified pipeline by loading its configuration and executing its tasks.

    :param pipeline_name: The name of the pipeline to run.
    :param pipelines_file_path: The path to the JSON file containing the pipelines configuration.
    :raises ValueError: If the specified pipeline is not found in the configuration.
    :return: None
    """

    pipelines = load_pipeline_config(pipelines_file_path)
    # Busca el pipeline con el nombre indicado
    pipeline = next((p for p in pipelines['pipelines'] if p['name'] == pipeline_name), None)
    
    if not pipeline:
        raise ValueError(f"Pipeline '{pipeline_name}' not found.")
    
    print(f"Running pipeline {pipeline_name}")
    
    for task in pipeline['tasks']:
        task_path = task['task']['task_path']
        base_parameters = task['task']['base_parameters']
        print(f"Executing task {task['task_key']} in pipeline {pipeline_name}")
        execute_task(task_path, base_parameters)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python main.py <pipeline_name>")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    pipelines_file_path = os.path.join(script_dir, "pipelines.json")
    pipeline_name = sys.argv[1]
    
    try:
        run_pipeline(pipeline_name, pipelines_file_path)
    except Exception as e:
        print(f"Error: {e}")