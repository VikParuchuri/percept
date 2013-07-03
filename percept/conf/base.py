"""
Application level configuration and logging
"""

import os
import global_settings
import sys
from logging.config import dictConfig
from importlib import import_module

import logging
log = logging.getLogger(__name__)

class Settings(object):
    """
    Configuration class for percept
    """
    settings_list = None

    def _initialize(self, settings_module):
        """
        Initialize the settings from a given settings_module
        settings_module - path to settings module
        """
        #Get the global settings values and assign them as self attributes
        self.settings_list = []
        for setting in dir(global_settings):
            #Only get upper case settings
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))
                self.settings_list.append(setting)

        #If a settings module was passed in, import it, and grab settings from it
        #Overwrite global settings with theses
        if settings_module is not None:
            self.SETTINGS_MODULE = settings_module

            #Try to import the settings module
            try:
                mod = import_module(self.SETTINGS_MODULE)
            except ImportError:
                error_message = "Could not import settings at {0}".format(self.SETTINGS_MODULE)
                log.exception(error_message)
                raise ImportError(error_message)

            #Grab uppercased settings as set them as self attrs
            for setting in dir(mod):
                if setting == setting.upper():
                    if setting == "INSTALLED_APPS":
                        self.INSTALLED_APPS += getattr(mod, setting)
                    else:
                        setattr(self, setting, getattr(mod, setting))
                    self.settings_list.append(setting)

        #If PATH_SETTINGS is in the settings file, extend the system path to include it
        if hasattr(self, "PATH_SETTINGS"):
            for path in self.PATH_SETTINGS:
                sys.path.extend(getattr(self,path))

        self.settings_list = list(set(self.settings_list))

    def _setup(self):
        """
        Perform initial setup of the settings class, such as getting the settings module and setting the settings
        """
        settings_module  = None
        #Get the settings module from the environment variables
        try:
            settings_module = os.environ[global_settings.MODULE_VARIABLE]
        except KeyError:
            error_message = "Settings not properly configured.  Cannot find the environment variable {0}".format(global_settings.MODULE_VARIABLE)
            log.exception(error_message)

        self._initialize(settings_module)
        self._configure_logging()

    def __getattr__(self, name):
        """
        If a class is trying to get settings (attributes on this class)
        """
        #If settings have not been setup, do so
        if not self.configured:
            self._setup()

        #Return setting if it exists as a self attribute, None if it doesn't
        if name in self.settings_list:
            return getattr(self, name)
        else:
            return None

    def _configure_logging(self):
        """
        Setting up logging from logging config in settings
        """
        if not self.LOGGING_CONFIG:
            #Fallback to default logging in global settings if needed
            dictConfig(self.DEFAULT_LOGGING)
        else:
            dictConfig(self.LOGGING_CONFIG)

    @property
    def configured(self):
        return self.settings_list is not None

#Import this if trying to get settings elsewhere
settings = Settings()