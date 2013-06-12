import pkgutil
from importlib import import_module
from collections import namedtuple
from conf.base import settings
import logging
log = logging.getLogger(__name__)

class RegistryCategories(object):
    base = "base"
    preprocessors = "preprocessors"
    inputs = "inputs"
    dataformats = "dataformats"

RegistryEntry = namedtuple('RegistryEntry', ['category', 'namespace', 'name', 'cls'], verbose=True)

def register(cls):
    registry_entry = RegistryEntry(category = cls.category, namespace = cls.namespace, name = cls.name, cls=cls)
    if registry_entry not in registry:
        registry.append(registry_entry)

def find_in_registry(category = None, namespace = None, name = None):
    selected_registry = registry
    if category is not None:
        selected_registry = [re for re in selected_registry if re.category==category]
    if namespace is not None:
        selected_registry = [re for re in selected_registry if re.namespace==namespace]
    if name is not None:
        selected_registry = [re for re in selected_registry if re.name==name]
    if len(selected_registry)>0:
        return [sr.cls for sr in selected_registry]

    return None

def import_task_modules(installed_apps):
    top_level_modules = installed_apps
    modules = []
    for module in top_level_modules:
        mod = import_module(module)
        for loader, module_name, is_pkg in  pkgutil.walk_packages(mod.__path__):
            if not module_name.startswith("__"):
                module = loader.find_module(module_name).load_module(module_name)
                modules.append(module)
    return modules

registry = []
import_task_modules(settings.INSTALLED_APPS)
