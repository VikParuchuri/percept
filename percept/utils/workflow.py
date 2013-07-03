from percept.utils.registry import registry, find_in_registry
from percept.conf.base import settings
from percept.utils.input import import_from_string
from percept.utils.models import get_task_name
import ConfigParser

class WorkflowLoader(object):
    """
    Loads and saves workflows
    """
    store = import_from_string(settings.DATASTORE)

    def __init__(self):
        self.store = self.store()

    def load(self, cls, run_id):
        """
        Load a workflow
        cls - workflow class (to get __name__ from)
        run_id - id given to the specific run
        """
        id_code = self.generate_load_identifier(cls, run_id)
        inst = self.store.load(id_code)
        return inst

    def save(self, obj, run_id):
        """
        Save a workflow
        obj - instance of a workflow to save
        run_id - unique id to give the run
        """
        id_code = self.generate_save_identifier(obj, run_id)
        self.store.save(obj, id_code)

    def save_predictions(self, obj, run_id):
        id_code = self.generate_prediction_save_identifier(obj, run_id)
        self.store.save(obj, id_code)

    def generate_save_identifier(self, obj, run_id):
        identifier = "{0}-{1}".format(get_task_name(obj), run_id)
        return identifier

    def generate_prediction_save_identifier(self, obj, run_id):
        identifier = "{0}_predictions".format(run_id)
        return identifier

    def generate_load_identifier(self, cls, run_id):
        identifier = "{0}-{1}".format(get_task_name(cls), run_id)
        return identifier

class WorkflowWrapper(object):
    """
    Wraps a workflow for convenience
    """
    #Needed to convert relative to absolute paths
    config_file_format = "{0}/../{1}"

    def __init__(self, config_file, workflow):
        """
        workflow - a workflow class, such as NaiveWorkflow
        config_file - path to a configuration file
        """
        #Create a configuration parser and parse config file
        config = ConfigParser.SafeConfigParser()
        config.read(config_file)

        #Read values from config file
        self.input_file = self.reformat_filepath(config_file, config.get('inputs', 'file'))
        self.input_format = config.get('inputs', 'format')

        self.target_file = self.reformat_filepath(config_file, config.get('targets', 'file'))
        self.target_format = config.get('targets', 'format')

        #Tasks is a list, so split by comma
        task_names = config.get('tasks', 'list')
        self.task_names = task_names.split(",")

        self.run_id = config.get('meta', 'run_id')
        self.save_flow = config.get('meta', 'save_flow').lower() == "true"
        self.load_previous_flow = config.get('meta', 'load_previous_flow').lower() == "true"
        self.predict = config.get('meta', 'predict').lower() == "true"

        self.predict_file = None
        self.predict_format = None
        if self.predict:
            self.predict_file = self.reformat_filepath(config_file, config.get('predict', 'file'))
            self.predict_format = config.get('predict', 'format')

        self.workflow_loader = WorkflowLoader()
        self.workflow = workflow

    def setup_tasks(self, tasks):
        """
        Find task classes from category.namespace.name strings
        tasks - list of strings
        """
        task_classes = []
        for task in tasks:
            category, namespace, name = task.split(".")
            cls = find_in_registry(category=category, namespace=namespace, name=name)[0]
            task_classes.append(cls)
        self.tasks = task_classes

    def initialize_workflow(self, workflow):
        """
        Create a workflow
        workflow - a workflow class
        """
        self.workflow = workflow()
        self.workflow.tasks = self.tasks

        self.workflow.input_file = self.input_file
        self.workflow.input_format = self.input_format
        self.workflow.target_file = self.target_file
        self.workflow.target_format = self.target_format
        self.workflow.run_id = self.run_id

        self.workflow.setup()

    def reformat_filepath(self, config_file, filename):
        """
        Convert relative paths in config file to absolute
        """
        if not filename.startswith("/"):
            filename = self.config_file_format.format(config_file, filename)
        return filename

    def run(self):
        if self.load_previous_flow:
            self.load()
        else:
           self.train_workflow()
        if self.save_flow:
            self.save()
        if self.predict:
            self.workflow.predict_file = self.predict_file
            self.workflow.predict_format = self.predict_format
            predictions = self.predict_workflow()
            self.save_predictions(predictions)

    def predict_workflow(self):
        return self.workflow.predict()

    def train_workflow(self):
        self.setup_tasks(self.task_names)
        self.initialize_workflow(self.workflow)
        self.workflow.train()

    def save(self):
        self.workflow_loader.save(self.workflow, self.run_id)

    def load(self):
        self.workflow = self.workflow_loader.load(self.workflow, self.run_id)

    def save_predictions(self, predictions):
        self.workflow_loader.save_predictions(predictions, self.run_id)
