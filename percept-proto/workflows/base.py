from utils.input import import_from_string, DataFormats
from collections import namedtuple

TrainedDependency = namedtuple('DependencyResult', ['category', 'namespace', 'name', 'inst'], verbose=True)

class BaseWorkflow(object):
    runner = import_from_string(settings.RUNNER)()
    input_file = ""
    input_format = DataFormats.csv
    tasks = []

    def __init__(self, **kwargs):
        pass

    def setup(self, tasks, **kwargs):
        self.tasks = tasks

    def find_dependencies(self, task):
        dependencies = task.dependencies
        return dependencies

    def execute_train_task_with_dependencies(self, task_cls, **kwargs):
        task_inst = task_cls()
        if hasattr(task_inst, "dependencies"):
            deps = task_inst.dependencies
            dep_results = []
            for dep in deps:
                dep_results.append(self.execute_train_task_with_dependencies(dep, **kwargs))
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
        result = task_inst.predict(**kwargs)
        return result

    def train(self, **kwargs):
        self.trained_tasks = []
        for task in self.tasks:
            self.trained_tasks.append(self.execute_train_task_with_dependencies(task, **kwargs))

    def predict(self, **kwargs):
        results = []
        for task_inst in self.trained_tasks:
            results.append(self.execute_predict_task(task_inst, **kwargs))
        return results

    def read_input(self, input_cls, **kwargs):
        input_data = open(self.input_file)
        input_inst = input_cls()
        input_inst.read_input(input_data)
        return input_inst.get_data()

    def reformat_input(self, input_data, input_format, output_format, **kwargs):
        needed_formats = []
        for task_cls in self.tasks:
            needed_formats.append(task_cls.data_format)
        needed_formats = list(set(needed_formats))


class NaiveWorkflow(BaseWorkflow):
    pass
