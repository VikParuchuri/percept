"""
Allow for the creation of custom command line commands
"""

from optparse import make_option, OptionParser
import sys
import os

def handle_default_options(options):
    """
    Pass in a Values instance from OptionParser.  Handle settings and pythonpath
    options - Values from OptionParser
    """
    if options.settings:
        #Set the percept_settings_module (picked up by settings in conf.base)
        os.environ['PERCEPT_SETTINGS_MODULE'] = options.settings
    if options.pythonpath:
        #Append the pythonpath and the directory one up from the pythonpath to sys.path for importing
        pythonpath = os.path.abspath(options.pythonpath)
        up_one_path = os.path.abspath(os.path.join(pythonpath, ".."))
        sys.path.append(pythonpath)
        sys.path.append(up_one_path)

class BaseCommand(object):
    """
    All commands inherit from this class
    """
    #Allowed options
    option_list = (
        make_option('--settings',
                    help='The Python path to a settings module, e.g. "myproject.settings.main".'),
        make_option('--pythonpath',
                    help='A directory to add to the Python path'),
    )
    command_help = ''
    args = ''

    def usage(self, subcommand):
        """
        Print the usage for a given subcommand
        """
        usage = '%%prog %s [options] %s' % (subcommand, self.args)
        return usage

    def create_parser(self, prog_name, subcommand):
        """
        Create an OptionParser
        prog_name - Name of a command
        subcommand - Name of a subcommand
        """
        parser = OptionParser(prog=prog_name,
                              usage=self.usage(subcommand),
                              option_list=self.option_list)
        return parser

    def print_help(self, prog_name, subcommand):
        """
        Print the help that the parser generates
        prog_name - Name of a command
        subcommand - Name of a subcommand
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        """
        Given certain command line arguments, run the basecommand
        argv - command line arguments
        """
        parser = self.create_parser(argv[0], argv[1])
        options, args = parser.parse_args(argv[2:])
        handle_default_options(options)
        self.execute(*args, **options.__dict__)

    def execute(self, *args, **options):
        from percept.conf.base import settings
        self.command(*args, **options)

    def command(self, *args, **options):
        """
        Overridden by the class that inherits from this.  Contains logic to run the command.
        """
        raise NotImplementedError()