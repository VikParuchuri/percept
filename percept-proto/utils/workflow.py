from utils.registry import registry, find_in_registry
import ConfigParser

class WorkflowWrapper(object):
    """
    Wraps a workflow
    """
    config_file_format = "{0}/../{1}"

    def __init__(self, config_file, workflow):
        config = ConfigParser.SafeConfigParser()
        config.read(config_file)

        self.input_file = self.reformat_filepath(config_file, config.get('inputs', 'file'))
        self.input_format = config.get('inputs', 'format')

        self.target_file = self.reformat_filepath(config_file, config.get('targets', 'file'))
        self.target_format = config.get('targets', 'format')

        tasks = config.get('tasks', 'list')
        tasks = tasks.split(",")

        self.run_id = config.get('tasks', 'run_id')

        self.setup_tasks(tasks)
        self.initialize_workflow(workflow)

    def setup_tasks(self, tasks):
        task_classes = []
        for task in tasks:
            category, namespace, name = task.split(".")
            cls = find_in_registry(category=category, namespace=namespace, name=name)[0]
            task_classes.append(cls)
        self.tasks = task_classes

    def initialize_workflow(self, workflow):
        self.workflow = workflow()
        self.workflow.tasks = self.tasks

        self.workflow.input_file = self.input_file
        self.workflow.input_format = self.input_format
        self.workflow.target_file = self.target_file
        self.workflow.target_format = self.target_format
        self.workflow.run_id = self.run_id

        self.workflow.setup()

    def reformat_filepath(self, config_file, filename):
        if not filename.startswith("/"):
            filename = self.config_file_format.format(config_file, filename)
        return filename
