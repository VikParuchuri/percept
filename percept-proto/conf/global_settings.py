from path import path
import os

#Various paths
FOLDER_PATH = path(__file__).dirname()
PACKAGE_PATH = FOLDER_PATH.dirname()
REPO_PATH = PACKAGE_PATH.dirname()

#Where to cache values during the run
CACHE = "percept-proto.fields.caches.MemoryCache"
#Do we use json to serialize the values in in the cache?
SERIALIZE_CACHE_VALUES = False

#How to run the workflows
RUNNER = "percept-proto.workflows.runners.SingleThreadedRunner"

#What to use as a datastore
DATASTORE = "percept-proto.workflows.datastores.FileStore"

#Append these settings to sys.path
PATH_SETTINGS = ["REPO_PATH", "PACKAGE_PATH"]

#Environment variable specifying where to find the settings
MODULE_VARIABLE = "PERCEPT_SETTINGS_MODULE"

#Namespace to give the modules in the registry
NAMESPACE = "percept"

#Can be used as a prefix when saving workflows
RUN_ID = "run1"

#Used to save and retrieve workflows and other data
DATA_PATH = os.path.abspath(os.path.join(REPO_PATH, "stored_data"))
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

#Commands are discovered here, and tasks/inputs/formats are imported using only these modules
INSTALLED_APPS = [
    'percept-proto.datahandlers',
    'percept-proto.tasks',
    'percept-proto.workflows',
    'percept-proto.tests'
]

#Setup logger configuration
DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        'percept': {
            'handlers': ['console', 'file'],
            },
        }
}

