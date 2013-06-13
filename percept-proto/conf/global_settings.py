from path import path

REPO_PATH = path(__file__).dirname()
ENV_ROOT = REPO_PATH.dirname()

DATASTORE = "percept-proto.fields.datastores.MemoryStore"
RUNNER = "percept-proto.workflows.runners.SingleThreadedRunner"

PATH_SETTINGS = ["REPO_PATH", "ENV_ROOT"]

MODULE_VARIABLE = "PERCEPT_SETTINGS_MODULE"

NAMESPACE = "percept"

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

