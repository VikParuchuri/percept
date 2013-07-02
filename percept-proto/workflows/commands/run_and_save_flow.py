from management.commands import BaseCommand
from utils.registry import registry, find_in_registry
from workflows.base import NaiveWorkflow, WorkflowLoader
from utils.workflow import WorkflowWrapper
import ConfigParser

import logging
log = logging.getLogger(__name__)

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


