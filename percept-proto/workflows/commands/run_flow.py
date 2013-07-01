from management.commands import BaseCommand

class Command(BaseCommand):
    def command(self, *args, **options):
        print "command"