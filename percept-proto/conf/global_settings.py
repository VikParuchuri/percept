from path import path
import os

FOLDER_PATH = path(__file__).dirname()
PACKAGE_PATH = FOLDER_PATH.dirname()
REPO_PATH = PACKAGE_PATH.dirname()

CACHE = "percept-proto.fields.caches.MemoryCache"
RUNNER = "percept-proto.workflows.runners.SingleThreadedRunner"
DATASTORE = "percept-proto.workflows.datastores.MemoryStore"

PATH_SETTINGS = ["REPO_PATH", "PACKAGE_PATH"]

MODULE_VARIABLE = "PERCEPT_SETTINGS_MODULE"

NAMESPACE = "percept"

RUN_ID = "run1"

DATA_PATH = os.path.abspath(os.path.join(REPO_PATH, "stored_data"))
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

INSTALLED_APPS = [
    'percept-proto.datahandlers',
    'percept-proto.tasks'
]

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'brief',
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

