from utils.registry import registry, find_in_registry
from workflows.base import NaiveWorkflow

class WorkflowWrapper(object):
    """
    Wraps a workflow
    """
    workflow = NaiveWorkflow

    def __init__(self, input_file, input_format, target_file, target_format, tasks, run_id):
        self.input_file = input_file
        self.input_format = input_format
        self.target_file = target_file
        self.target_format = target_format
        self.run_id = run_id

        self.setup_tasks(tasks)
        self.initialize_workflow()

    def setup_tasks(self, tasks):
        task_classes = []
        for task in tasks:
            category, namespace, name = task.split(".")
            cls = find_in_registry(category=category, namespace=namespace, name=name)[0]
            task_classes.append(cls)
        self.tasks = task_classes

    def initialize_workflow(self):
        self.workflow = self.workflow()
        self.workflow.tasks = self.tasks

        self.workflow.input_file = self.input_file
        self.workflow.input_format = self.input_format
        self.workflow.target_file = self.target_file
        self.workflow.target_format = self.target_format
        self.workflow.run_id = self.run_id

        self.workflow.setup()
