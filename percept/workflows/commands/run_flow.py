"""
Given a config file, run a given workflow
"""

from percept.management.commands import BaseCommand
from percept.utils.registry import registry, find_in_registry
from percept.workflows.base import NaiveWorkflow
from percept.utils.workflow import WorkflowWrapper, WorkflowLoader

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    args = 'config_file'

    def command(self, *args, **options):
        config_file = args[0]

        wrapper = WorkflowWrapper(config_file, NaiveWorkflow)
        wrapper.run()

