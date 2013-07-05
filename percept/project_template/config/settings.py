"""
Settings for project_template
"""

from path import path
import os
import sys

#Various paths
PROJECT_PATH = path(__file__).dirname().dirname()

#Where to cache values during the run
CACHE = "percept.fields.caches.MemoryCache"
#Do we use json to serialize the values in in the cache?
SERIALIZE_CACHE_VALUES = False

#How to run the workflows
RUNNER = "percept.workflows.runners.SingleThreadedRunner"

#What to use as a datastore
DATASTORE = "percept.workflows.datastores.FileStore"

#Namespace to give the modules in the registry
NAMESPACE = "project_template"

#What severity of error to log to file and console.  One of "DEBUG", "WARN", "INFO", "ERROR"
LOG_LEVEL = "DEBUG"

#Used to save and retrieve workflows and other data
DATA_PATH = os.path.abspath(os.path.join(PROJECT_PATH, "stored_data"))
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

#Commands are discovered here, and tasks/inputs/formats are imported using only these modules
INSTALLED_APPS = [
    'project_template.inputs',
    'project_template.formatters',
    'project_template.tasks',
    'project_template.workflows'
]