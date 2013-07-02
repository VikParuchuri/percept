import nose
from management.commands import BaseCommand
from conf.base import settings

class Command(BaseCommand):
    def command(self, *args, **options):
        #Grab the pythonpath argument and look for tests there
        app_names = settings.INSTALLED_APPS
        app_labels = list(set(["--cover-package={0}".format(a.split('.')[0]) for a in app_names]))
        argv = ['{0}'.format(options['pythonpath']), '--with-coverage', ' '.join(app_labels)]
        nose.run(argv=argv)