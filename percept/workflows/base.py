"""
Workflows allow us to run tasks
"""

from utils.input import import_from_string, DataFormats
from utils.models import find_needed_formatter, find_needed_input, RegistryCategories, MetaFieldModel, get_task_name
from collections import namedtuple
from conf.base import settings
from tests.framework import NaiveWorkflowTester
import logging
import os

log = logging.getLogger(__name__)

TrainedDependency = namedtuple('DependencyResult', ['category', 'namespace', 'name', 'inst'], verbose=False)

class BaseWorkflow(object):
    """
    Base workflow class
    """
    #Metaclass needed to register the workflow
    __metaclass__ = MetaFieldModel
    #category, namespace, name for the registry
    category = RegistryCategories.base
    namespace = settings.NAMESPACE
    name = __name__.lower()

    #Defines how tasks are run
    runner = import_from_string(settings.RUNNER)
    input_file = ""
    input_format = DataFormats.csv
    target_file = ""
    target_format = DataFormats.csv
    predict_file = ""
    predict_format = DataFormats.csv
    tasks = []
    run_id = ""
    help_text = "Base class for workflow.  Do not use directly."

    def __init__(self, **kwargs):
        #initialize runner.  Don't do this at class level to avoid sharing same runner object.
        self.runner = self.runner()
        self.setup_run = False

    def setup(self):
        #Reformat input data as needed
        self.reformatted_input = self.reformat_input()
        self.setup_run = True

    def find_dependencies(self, task):
        dependencies = task.dependencies
        return dependencies

    def execute_train_task_with_dependencies(self, task_cls, **kwargs):
        """
        Run the training, as well as any dependencies of the training
        task_cls - class of a task
        """
        log.info("Task {0}".format(get_task_name(task_cls)))
        #Instantiate the task
        task_inst = task_cls()
        #Grab arguments from the task instance and set them
        for arg in task_inst.args:
            if arg not in kwargs:
                kwargs[arg] = task_inst.args[arg]
        #Check for dependencies defined by the task
        if hasattr(task_inst, "dependencies"):
            deps = task_inst.dependencies
            dep_results = []
            #Run the dependencies through recursion (in case of dependencies of dependencies, etc)
            for dep in deps:
                log.info("Dependency {0}".format(get_task_name(dep)))
                dep_results.append(self.execute_train_task_with_dependencies(dep.cls, **dep.args))
            trained_dependencies = []
            #Add executed dependency to trained_dependencies list on the task
            for i in xrange(0,len(deps)):
                dep = deps[i]
                dep_result = dep_results[i]
                name = dep.name
                namespace = dep.namespace
                category = dep.category
                trained_dependencies.append(TrainedDependency(category=category, namespace=namespace, name = name, inst = dep))
            task_inst.trained_dependencies = trained_dependencies
        #Finally, run the task
        task_inst.train(**kwargs)
        return task_inst

    def execute_predict_task(self, task_inst, predict_data, **kwargs):
        """
        Do a prediction
        task_inst - instance of a task
        """
        result = task_inst.predict(predict_data, **task_inst.args)
        return result

    def train(self, **kwargs):
        """
        Do the workflow training
        """
        log.info("Starting to train...")
        if not self.setup_run:
            self.setup()
        self.trained_tasks = []
        for task in self.tasks:
            data = self.reformatted_input[task.data_format]['data']
            target = self.reformatted_input[task.data_format]['target']
            kwargs['data']=data
            kwargs['target']=target
            trained_task = self.execute_train_task_with_dependencies(task, **kwargs)
            self.trained_tasks.append(trained_task)

            #If the trained task alters the data in any way, pass it down the chain to the next task
            if hasattr(trained_task, 'data'):
                self.reformatted_input[task.data_format]['data'] = trained_task.data
        log.info("Finished training.")

    def predict(self, **kwargs):
        """
        Do the workflow prediction (done after training, with new data)
        """
        reformatted_predict = self.reformat_predict_data()
        results = {}
        for task_inst in self.trained_tasks:
            predict = reformatted_predict[task_inst.data_format]['predict']
            kwargs['predict']=predict
            results.update({get_task_name(task_inst) : self.execute_predict_task(task_inst, predict, **kwargs)})
        return results

    def find_input(self, input_format):
        """
        Find an input class for a given format
        input_format - see utils.input.dataformats
        """
        input_cls = find_needed_input(input_format)
        return input_cls

    def read_input(self, input_cls, filename, **kwargs):
        """
        Read in input and do some minimal preformatting
        input_cls - the class to use to read the input
        filename - input filename
        """
        input_data = open(filename)
        input_inst = input_cls()
        input_inst.read_input(input_data)
        return input_inst.get_data()

    def reformat_file(self, input_file, input_format, output_format):
        """
        Reformat input data files to a format the tasks can use
        """
        #Return none if input_file or input_format do not exist
        if input_file is None or input_format is None:
            return None
        #Find the needed input class and read the input stream
        try:
            input_cls = self.find_input(input_format)
            input_inst = input_cls()
        except TypeError:
            #Return none if input_cls is a Nonetype
            return None
        #If the input file cannot be found, return None
        try:
            input_inst.read_input(self.open_file(input_file))
        except IOError:
            return None

        formatter = find_needed_formatter(input_format, output_format)
        if formatter is None:
            raise Exception("Cannot find a formatter that can convert from {0} to {1}".format(self.input_format, output_format))
        formatter_inst = formatter()
        formatter_inst.read_input(input_inst.get_data(), input_format)
        data = formatter_inst.get_data(output_format)
        return data

    def open_file(self, input_file):
        """
        Open the input file
        """
        #abspath needed to avoid relative path issues
        return open(os.path.abspath(input_file))

    def reformat_predict_data(self, **kwargs):
        reformatted_predict = {}
        for output_format in self.needed_formats:
            reformatted_predict.update(
                {
                    output_format :
                        {
                            'predict' : self.reformat_file(self.predict_file, self.predict_format, output_format),
                        }
                }
            )
        return reformatted_predict

    def reformat_input(self, **kwargs):
        """
        Reformat input data
        """
        reformatted_input = {}
        needed_formats = []
        for task_cls in self.tasks:
            needed_formats.append(task_cls.data_format)
        self.needed_formats = list(set(needed_formats))

        for output_format in self.needed_formats:
            reformatted_input.update(
                {
                    output_format :
                        {
                        'data' : self.reformat_file(self.input_file, self.input_format, output_format),
                        'target' : self.reformat_file(self.target_file, self.target_format, output_format)
                        }
                }
            )
        return reformatted_input

class NaiveWorkflow(BaseWorkflow):
    """
    Naive workflow that doesn't optimize anything
    """
    category = RegistryCategories.workflows
    tester = NaiveWorkflowTester
    test_cases = [
        {'config_file' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/workflow_config/test_save.conf'))},
        {'config_file' : os.path.abspath(os.path.join(settings.PACKAGE_PATH,'tests/workflow_config/test_load.conf'))}
    ]
    help_text = "Naive workflow class that is not optimized."
