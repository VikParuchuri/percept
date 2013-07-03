"""
Default settings that can be overridden with custom settings files
"""

from path import path
import os
import sys

#Various paths
FOLDER_PATH = path(__file__).dirname()
PACKAGE_PATH = FOLDER_PATH.dirname()
REPO_PATH = PACKAGE_PATH.dirname()

#Where to cache values during the run
CACHE = "percept.fields.caches.MemoryCache"
#Do we use json to serialize the values in in the cache?
SERIALIZE_CACHE_VALUES = False

#How to run the workflows
RUNNER = "percept.workflows.runners.SingleThreadedRunner"

#What to use as a datastore
DATASTORE = "percept.workflows.datastores.FileStore"

#Append these settings to sys.path
PATH_SETTINGS = ["REPO_PATH", "PACKAGE_PATH"]

#Environment variable specifying where to find the settings
MODULE_VARIABLE = "PERCEPT_SETTINGS_MODULE"

#Namespace to give the modules in the registry
NAMESPACE = "percept"

#Used to save and retrieve workflows and other data
DATA_PATH = os.path.abspath(os.path.join(REPO_PATH, "stored_data"))
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

#What severity of error to log to file and console.  One of "DEBUG", "WARN", "INFO", "ERROR"
LOG_LEVEL = "DEBUG"

#Modules to not include in coverage stats
DO_NOT_COVER = ["conf", "management"]

#Commands are discovered here, and tasks/inputs/formats are imported using only these modules
INSTALLED_APPS = [
    'percept.datahandlers',
    'percept.tasks',
    'percept.workflows',
    'percept.tests'
]

#Setup logger configuration
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters' : {
        'precise' : {
            'format' : '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'verbose' : {
            'format' : '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'brief' : {
            'format' : '%(asctime)s - %(name)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'precise',
            },
        'file': {
            'level': 'DEBUG',
            'formatter': 'precise',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'percept.log'
            },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'propagate' : True,
            'level' : LOG_LEVEL
            },
        }
}

