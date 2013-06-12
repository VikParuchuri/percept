import conf.base
import pkgutil
from importlib import import_module
from utils.models import registry
import logging
log = logging.getLogger(__name__)

def import_task_modules():
    top_level_modules = conf.base.settings.INSTALLED_APPS
    module_names = []
    for module in top_level_modules:
        mod = import_module(module)
        for loader, module_name, is_pkg in  pkgutil.walk_packages(mod.__path__):
            if not module_name.startswith("__"):
                submod_name = "{0}.{1}".format(module,module_name)
                module_names.append(submod_name)
    modules = map(import_module, module_names)
    return modules

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

import_task_modules()

