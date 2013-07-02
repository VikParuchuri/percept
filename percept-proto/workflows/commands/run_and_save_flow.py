from management.commands import BaseCommand
from utils.registry import registry, find_in_registry
from workflows.base import NaiveWorkflow, WorkflowLoader
from conf.base import settings
import ConfigParser

import logging
log = logging.getLogger(__name__)

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

class Command(BaseCommand):
    args = 'config_file'
    config_file_format = "{0}/../{1}"

    def command(self, *args, **options):
        config_file = args[0]
        config = ConfigParser.SafeConfigParser()
        config.read(config_file)

        input_file = self.reformat_filepath(config_file, config.get('inputs', 'file'))
        input_format = config.get('inputs', 'format')

        target_file = self.reformat_filepath(config_file, config.get('targets', 'file'))
        target_format = config.get('targets', 'format')

        tasks = config.get('tasks', 'list')
        tasks = tasks.split(",")

        run_id = config.get('tasks', 'run_id')
        wrapper = WorkflowWrapper(input_file, input_format, target_file, target_format, tasks, run_id)
        wrapper.workflow.train()

        loader = WorkflowLoader()
        loader.save(wrapper.workflow, run_id)

    def reformat_filepath(self, config_file, filename):
        if not filename.startswith("/"):
            filename = self.config_file_format.format(config_file, filename)
        return filename


