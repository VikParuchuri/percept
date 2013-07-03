"""
Allows for command line commands to be run and defined
"""

from optparse import OptionParser
import sys
import os
import imp
from commands import BaseCommand, handle_default_options
from importlib import import_module

import logging
log = logging.getLogger(__name__)

def find_all_commands(management_dir):
    """
    Find all valid commands in a directory
    management_dir : directory path
    return - List of commands
    """
    try:
        #Find all commands in the directory that are not __init__.py and end in .py.  Then, remove the trailing .py
        return [f[:-3] for f in os.listdir(management_dir) if f.endswith('.py') and not f.startswith("__")]
    except OSError:
        #If nothing is found, return empty
        return []

def find_commands_module(app_name):
    """
    Find the commands module in each app (if it exists) and return the path
    app_name : The name of an app in the INSTALLED_APPS setting
    return - path to the app
    """
    parts = app_name.split('.')
    parts.append('commands')
    parts.reverse()
    part = parts.pop()
    path = None

    #Load the module if needed
    try:
        f, path, descr = imp.find_module(part, path)
    except ImportError as e:
        if os.path.basename(os.getcwd()) != part:
            raise e
        else:
            if f:
                f.close()

    #Go down level by and level and try to load the module at each level
    while parts:
        part = parts.pop()
        f, path, descr = imp.find_module(part, [path] if path else None)
        if f:
            f.close()
    return path


def get_commands():
    """
    Get all valid commands
    return - all valid commands in dictionary form
    """
    commands = {}

    #Try to load the settings file (settings can be specified on the command line) and get the INSTALLED_APPS
    try:
        from percept.conf.base import settings
        apps = settings.INSTALLED_APPS
    except KeyError:
        apps = []

    #For each app, try to find the command module (command folder in the app)
    #Then, try to load all commands in the directory
    for app_name in apps:
        try:
            path = find_commands_module(app_name)
            commands.update(dict([(name, app_name) for name in find_all_commands(path)]))
        except ImportError as e:
            pass

    return commands

def load_command_class(app_name, name):
    """
    Load the command class in a given module
    app_name - string app name
    name - python file name that contains a class called Command that inherits from BaseCommand
    """
    module = import_module('%s.commands.%s' % (app_name, name))
    return module.Command()

class LaxOptionParser(OptionParser):
    """
    Parse options in a manner that does not do strict checking
    """
    def _process_args(self, largs, rargs, values):
        """
        Override process_args in OptionParser to avoid returning when arg cannot be processed
        """
        while rargs:
            arg = rargs[0]
            try:
                if arg[0:2] == "--" and len(arg) > 2:
                    self._process_long_opt(rargs, values)
                elif arg[:1] == "-" and len(arg) > 1:
                    self._process_short_opts(rargs, values)
                else:
                    del rargs[0]
                    raise Exception
            except Exception as e:
                print e
                largs.append(arg)

class Management(object):
    """
    Allow for management commands (command line) to be run
    """
    def __init__(self, argv=None):
        """
        Initialize with command line arguments
        argv - Command line arguments
        """
        #Get command line arguments when being instantiated
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def execute(self):
        """
        Run the command with the command line arguments
        """
        #Initialize the option parser
        parser = LaxOptionParser(
            usage="%prog subcommand [options] [args]",
            option_list=BaseCommand.option_list #This will define what is allowed input to the parser (ie --settings=)
        )

        #Parse the options
        options, args = parser.parse_args(self.argv)
        #Handle --settings and --pythonpath properly
        handle_default_options(options)

        try:
            #Get the name of the subcommand
            subcommand = self.argv[1]
        except IndexError:
            #If the subcommand name cannot be found, set it to help
            subcommand = 'help'

        #If the subcommand is help, print the usage of the parser, and available command names
        if subcommand == 'help':
            if len(args) <= 2:
                parser.print_help()
                sys.stdout.write(self.help_text + '\n')
        else:
            #Otherwise, run the given command
            self.fetch_command(subcommand).run_from_argv(self.argv)

    @property
    def help_text(self):
        """
        Formats and prints the help text from the command list
        """
        help_text = '\n'.join(sorted(get_commands().keys()))
        help_text = "\nCommands:\n" + help_text
        return help_text

    def fetch_command(self, subcommand):
        """
        Gets a given command
        """
        try:
            app_name = get_commands()[subcommand]
        except KeyError:
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" % \
                             (subcommand, self.prog_name))
            sys.exit(1)
        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, subcommand)
        return klass

def execute_from_command_line(argv=None):
    """
    Called by manage.py to run a command
    argv - Command line arguments
    """
    #pull in command line arguments and pass to management class
    manager = Management(argv)
    #Execute the manager
    manager.execute()