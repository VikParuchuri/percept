from utils.input import import_from_string, DataFormats
from utils.models import find_needed_formatter, find_needed_input
from collections import namedtuple
from conf.base import settings
import logging
import os

log = logging.getLogger(__name__)

TrainedDependency = namedtuple('DependencyResult', ['category', 'namespace', 'name', 'inst'], verbose=False)

class WorkflowLoader(object):
    """
    Loads and saves workflows
    """
    store = import_from_string(settings.DATASTORE)

    def __init__(self):
        self.store = self.store()

    def load(self, cls, run_id):
        id_code = self.generate_load_identifier(cls, run_id)
        inst = self.store.load(id_code)
        return inst

    def save(self, obj, run_id):
        id_code = self.generate_save_identifier(obj, run_id)
        self.store.save(obj, id_code)

    def generate_save_identifier(self, obj, run_id):
        identifier = "{0}-{1}".format(obj.__class__.__name__.lower(), run_id)
        return identifier

    def generate_load_identifier(self, cls, run_id):
        identifier = "{0}.{1}-{2}".format(cls.__module__.lower(), cls.__name__.lower(), run_id)
        return identifier

class BaseWorkflow(object):
    runner = import_from_string(settings.RUNNER)
    input_file = ""
    input_format = DataFormats.csv
    target_file = ""
    target_format = DataFormats.csv
    tasks = []

    def __init__(self, **kwargs):
        self.runner = self.runner()
        self.setup_run = False

    def setup(self):
        self.reformatted_input = self.reformat_input()
        self.setup_run = True

    def find_dependencies(self, task):
        dependencies = task.dependencies
        return dependencies

    def execute_train_task_with_dependencies(self, task_cls, **kwargs):
        log.info("Task {0}".format(task_cls.__name__))
        task_inst = task_cls()
        for arg in task_inst.args:
            if arg not in kwargs:
                kwargs[arg] = task_inst.args[arg]
        if hasattr(task_inst, "dependencies"):
            deps = task_inst.dependencies
            dep_results = []
            for dep in deps:
                log.info("Dependency {0}".format(dep.__name__))
                dep_results.append(self.execute_train_task_with_dependencies(dep.cls, **dep.args))
            trained_dependencies = []
            for i in xrange(0,len(deps)):
                dep = deps[i]
                dep_result = dep_results[i]
                name = dep.name
                namespace = dep.namespace
                category = dep.category
                trained_dependencies.append(TrainedDependency(category=category, namespace=namespace, name = name, inst = dep))
            task_inst.trained_dependencies = trained_dependencies
        task_inst.train(**kwargs)
        return task_inst

    def execute_predict_task(self, task_inst, **kwargs):
        result = task_inst.predict(**task_inst.args)
        return result

    def train(self, **kwargs):
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
        results = []
        for task_inst in self.trained_tasks:
            results.append(self.execute_predict_task(task_inst, **kwargs))
        return results

    def find_input(self, input_format):
        input_cls = find_needed_input(input_format)
        return input_cls

    def read_input(self, input_cls, filename, **kwargs):
        input_data = open(filename)
        input_inst = input_cls()
        input_inst.read_input(input_data)
        return input_inst.get_data()

    def reformat_file(self, input_file, input_format, output_format):

        #Find the needed input class and read the input stream
        input_cls = self.find_input(input_format)
        input_inst = input_cls()
        input_inst.read_input(self.open_file(input_file))

        formatter = find_needed_formatter(input_format, output_format)
        if formatter is None:
            raise Exception("Cannot find a formatter that can convert from {0} to {1}".format(self.input_format, output_format))
        formatter_inst = formatter()
        formatter_inst.read_input(input_inst.get_data(), input_format)
        data = formatter_inst.get_data(output_format)
        return data

    def open_file(self, input_file):
        return open(os.path.abspath(input_file))

    def reformat_input(self, **kwargs):
        reformatted_input = {}
        needed_formats = []
        for task_cls in self.tasks:
            needed_formats.append(task_cls.data_format)
        needed_formats = list(set(needed_formats))

        for output_format in needed_formats:
            reformatted_input.update(
                {
                    output_format :
                        {
                        'data' : self.reformat_file(self.input_file, self.input_format, output_format),
                        'target' : self.reformat_file(self.target_file, self.target_format, output_format),
                        }
                }
            )
        return reformatted_input

    def save(self, **kwargs):
        pass

class NaiveWorkflow(BaseWorkflow):
    pass
