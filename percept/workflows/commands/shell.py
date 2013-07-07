from percept.management.commands import BaseCommand

class Command(BaseCommand):
    help = "Runs a Python interactive interpreter."

    def command(self, **options):
        from IPython.frontend.terminal.ipapp import TerminalIPythonApp
        app = TerminalIPythonApp.instance()
        app.initialize(argv=[])
        app.start()
