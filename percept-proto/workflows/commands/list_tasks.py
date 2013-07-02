"""
List all available tasks
"""

from management.commands import BaseCommand
from utils.registry import registry, find_in_registry
from utils.models import get_task_name

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    args = ''

    def command(self, *args, **options):
        print "Available tasks:"
        print "        Name              -                 Help"
        for entry in registry:
            cls = entry.cls
            name = get_task_name(cls)
            help = getattr(cls, "help", "")
            print "{0} - {1}".format(name, help)


