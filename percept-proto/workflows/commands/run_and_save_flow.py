"""
Given a config file, run a given workflow
"""

from management.commands import BaseCommand
from utils.registry import registry, find_in_registry
from workflows.base import NaiveWorkflow, WorkflowLoader
from utils.workflow import WorkflowWrapper

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    args = 'config_file'

    def command(self, *args, **options):
        config_file = args[0]

        wrapper = WorkflowWrapper(config_file, NaiveWorkflow)
        wrapper.workflow.train()

        loader = WorkflowLoader()
        loader.save(wrapper.workflow, wrapper.run_id)


