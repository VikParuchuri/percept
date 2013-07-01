import nose
from management.commands import BaseCommand

class Command(BaseCommand):
    def command(self, *args, **options):
        #Grab the pythonpath argument and look for tests there
        argv = ['{0}'.format(options['pythonpath'])]
        nose.run(argv=argv)