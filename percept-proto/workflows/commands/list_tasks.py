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
        headers = ["Name", "Help"]
        help_table = []
        for entry in registry:
            cls = entry.cls
            name = get_task_name(cls)
            help_text = getattr(cls, "help_text", "")
            help_table.append([name, help_text])
        width = max([len(h[0]) for h in help_table])+5
        row_format =("{:<" +str(width) + "}") * (len(help_table[0]) + 1)
        print row_format.format("", *headers)
        for row in help_table:
            print row_format.format("", *row)


