from percept.management.commands import BaseCommand
import os
from importlib import import_module
from percept.conf.base import settings
import re

class Command(BaseCommand):
    args = 'name'
    def command(self, *args, **options):
        name = args[0]
        print "Starting to create project {0}...".format(name)
        #See if the module already exists somewhere
        try:
            import_module(name)
            raise Exception("Found module with name {0}".format(name))
        except ImportError:
            pass

        #Try to create the directory
        project_dir = os.path.join(os.getcwd(), name)
        try:
            os.makedirs(project_dir)
        except OSError:
            raise Exception("Could not make directory {0}".format(project_dir))

        folders_to_make = [name]

        for folder in folders_to_make:
            try:
                os.makedirs(os.path.join(project_dir, folder))
            except OSError:
                raise Exception("Could not make directory {0}".format(project_dir))

        project_template_dir = settings.PROJECT_TEMPLATE_DIR
        prefix_length = len(project_template_dir) + 1

        for root, dirs, files in os.walk(project_template_dir):
            path_end = root[prefix_length:]
            path_end = path_end.replace(settings.PROJECT_TEMPLATE_NAME, name)
            target_dir = os.path.join(project_dir, path_end)
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)

            for dirname in dirs[:]:
                if dirname.startswith('.') or dirname == '__pycache__':
                    dirs.remove(dirname)

            for filename in files:
                if filename.endswith('.pyc'):
                    continue
                old_path = os.path.join(root, filename)
                new_path = os.path.join(project_dir, path_end, filename)

                with open(old_path, 'rb') as template_file:
                    content = template_file.read()
                    content = content.replace(settings.PROJECT_TEMPLATE_NAME, name)
                with open(new_path, 'wb') as new_file:
                    new_file.write(content)
        print "Finished creating project {0}.".format(name)





