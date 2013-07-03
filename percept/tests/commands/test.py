"""
Command line command to run tests
"""

import nose
from percept.management.commands import BaseCommand
from percept.conf.base import settings
import pkgutil
from importlib import import_module
from optparse import make_option

import os

class Command(BaseCommand):
    args = 'cover'
    def command(self, *args, **options):
        try:
            cover = args[0]
            cover = cover.lower() == "true"
        except IndexError:
            cover = False
        if cover:
            #Grab the pythonpath argument and look for tests there
            app_names = settings.INSTALLED_APPS
            #Grab the top level app name from installed_apps
            app_labels = list(set([a.split('.')[0] for a in app_names]))
            app_paths = []
            #We want to figure out coverage for the "lower-level" apps, so import all the top level apps
            #and get their paths
            for al in app_labels:
                mod = import_module(al)
                app_paths.append(os.path.dirname(mod.__file__))
            #Pass paths to pkgutil to get the names of the submodules
            sub_labels = [name for _, name, _ in pkgutil.iter_modules(app_paths) if name not in settings.DO_NOT_COVER]
            #Produce a coverage report for installed_apps
            argv = ['{0}'.format(options['pythonpath']), '--with-coverage', '--cover-package={0}'.format(','.join(app_labels + sub_labels))]
            nose.run(argv=argv)
        else:
            argv = ['{0}'.format(options['pythonpath'])]
            nose.run(argv=argv)