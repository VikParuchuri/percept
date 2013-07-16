"""
Given a config file, run a given workflow
"""

from percept.management.commands import BaseCommand
from percept.utils.registry import registry, find_in_registry
from percept.workflows.base import NaiveWorkflow
from percept.utils.workflow import WorkflowWrapper, WorkflowLoader
from optparse import make_option
import IPython

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    args = 'config_file'

    option_list = BaseCommand.option_list + (make_option('--shell',
                                                         help='Whether or not to load a shell afterwards".'),)

    def command(self, *args, **options):
        config_file = args[0]

        wrapper = WorkflowWrapper(config_file, NaiveWorkflow)
        wrapper.run()

        if '--shell' in options:
            ns = {
                'flow' : wrapper.workflow,
                'tasks' : wrapper.workflow.tasks
            }

            IPython.embed(user_ns=ns)

