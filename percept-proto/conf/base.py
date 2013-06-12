import os
import global_settings
import sys
from logging.config import dictConfig
from importlib import import_module

import logging
log = logging.getLogger(__name__)

class Settings(object):
    settings_list = None
    def _initialize(self, settings_module):

        self.settings_list = []
        for setting in dir(global_settings):
            if setting == setting.upper():
                setattr(self, setting, getattr(global_settings, setting))
                self.settings_list.append(setting)

        if settings_module is not None:
            self.SETTINGS_MODULE = settings_module

            try:
                mod = import_module(self.SETTINGS_MODULE)
            except ImportError:
                error_message = "Could not import settings at {0}".format(self.SETTINGS_MODULE)
                log.exception(error_message)
                raise ImportError(error_message)

            for setting in dir(mod):
                if setting == setting.upper():
                    setattr(self, setting, getattr(mod, setting))
                    self.settings_list.append(setting)

        if hasattr(self, "PATH_SETTINGS"):
            for path in self.PATH_SETTINGS:
                sys.path.extend(getattr(self,path))

        self.settings_list = list(set(self.settings_list))

    def _setup(self):
        settings_module  = None
        try:
            settings_module = os.environ[global_settings.MODULE_VARIABLE]
        except KeyError:
            error_message = "Settings not properly configured.  Cannot find the environment variable {0}".format(global_settings.MODULE_VARIABLE)
            log.exception(error_message)

        self._initialize(settings_module)
        self._configure_logging()

    def __getattr__(self, name):
        if not self.configured:
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

    @property
    def configured(self):
        return self.settings_list is not None

settings = Settings()