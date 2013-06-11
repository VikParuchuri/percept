import os
import global_settings
import importlib
import sys
import logging

from logging.config import dictConfig

class Settings(object):
    settings_list = None
    def _initialize(self, settings_module):

        self.settings_list = []
        for setting in dir(global_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))
                self.settings_list.append(setting)

        if hasattr(global_settings, "PATH_SETTINGS"):
             for path in global_settings.PATH_SETTINGS:
                 sys.path.extend(path)

        self.SETTINGS_MODULE = settings_module

        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)
        except ImportError:
            error_message = "Could not import settings at {0}".format(self.SETTINGS_MODULE)
            raise ImportError(error_message)

        for setting in dir(mod):
            if setting == setting.upper():
                setattr(self, setting, getattr(mod, setting))
                self.settings_list.append(setting)

        self.settings_list = list(set(self.settings_list))

    def _setup(self):
        settings_module = os.environ[global_settings.MODULE_VARIABLE]
        if not settings_module:
            raise KeyError("Settings not properly configured.  Cannot find the environment variable {0}".format(global_settings.MODULE_VARIABLE))

        self._initialize(settings_module)
        self._configure_logging()

    def __getattr__(self, name):
        if self.settings_list is None:
            self._setup()
        if name in self.settings_list:
            return getattr(self, name)
        else:
            return None

    def _configure_logging(self):
        if self.LOGGING_CONFIG:
            dictConfig(self.DEFAULT_LOGGING)

            if self.LOGGING:
                dictConfig(self.LOGGING)