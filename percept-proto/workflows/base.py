from utils.input import import_from_string, DataFormats
from utils.models import find_needed_formatter, find_needed_input
from collections import namedtuple
from conf.base import settings

TrainedDependency = namedtuple('DependencyResult', ['category', 'namespace', 'name', 'inst'], verbose=True)

class BaseWorkflow(object):
    runner = import_from_string(settings.RUNNER)()
    input_file = ""
    input_format = DataFormats.csv
    target_file = ""
    target_format = DataFormats.csv
    tasks = []

    def __init__(self, **kwargs):
        self.input_data = self.read_input(self.find_input())
        self.reformatted_input = self.reformat_input(self.input_data)

    def setup(self, tasks, **kwargs):
        self.tasks = tasks

    def find_dependencies(self, task):
        dependencies = task.dependencies
        return dependencies

    def execute_train_task_with_dependencies(self, task_cls, **kwargs):
        task_inst = task_cls()
        for arg in task_inst.args:
            if arg not in kwargs:
                kwargs[arg] = task_inst.args[arg]
        if hasattr(task_inst, "dependencies"):
            deps = task_inst.dependencies
            dep_results = []
            for dep in deps:
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
        self.trained_tasks = []
        for task in self.tasks:
            data = self.reformatted_input[task.data_format]['data'].get_data()
            target = self.reformatted_input[task.data_format]['target'].get_data()
            kwargs['data']=data
            kwargs['target']=target
            self.trained_tasks.append(self.execute_train_task_with_dependencies(task, **kwargs))

    def predict(self, **kwargs):
        results = []
        for task_inst in self.trained_tasks:
            results.append(self.execute_predict_task(task_inst, **kwargs))
        return results

    def find_input(self):
        input_cls = find_needed_input(self.input_format)
        return input_cls

    def read_input(self, input_cls, filename, **kwargs):
        input_data = open(filename)
        input_inst = input_cls()
        input_inst.read_input(input_data)
        return input_inst.get_data()

    def reformat_input(self, input_data,  **kwargs):
        reformatted_input = {}
        needed_formats = []
        for task_cls in self.tasks:
            needed_formats.append(task_cls.data_format)
        needed_formats = list(set(needed_formats))
        for output_format in needed_formats:
            formatter = find_needed_formatter(self.input_format, output_format)
            if formatter is None:
                raise Exception("Cannot find a formatter that can convert from {0} to {1}".format(self.input_format, output_format))
            formatter_inst = formatter()
            formatter_inst.read_input(input_data, self.input_format, self.input_file)

            target_inst = formatter()
            target_inst.read_input(input_data, self.target_format, self.target_file)

            reformatted_input.update({output_format : {'data' : formatter_inst, 'target' : target_inst}})
        return reformatted_input

class NaiveWorkflow(BaseWorkflow):
    pass
