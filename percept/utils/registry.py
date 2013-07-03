"""
Search through modules and add to the registry
"""

from percept.conf.base import settings
import pkgutil
from importlib import import_module
from percept.utils.models import registry
import logging
log = logging.getLogger(__name__)

def import_task_modules():
    """
    Import all installed apps and add modules to registry
    """
    top_level_modules = settings.INSTALLED_APPS
    module_names = []
    for module in top_level_modules:
        #Import package
        mod = import_module(module)
        #Find all modules in package path
        for loader, module_name, is_pkg in  pkgutil.walk_packages(mod.__path__):
            if not module_name.startswith("__"):
                #If the module is not __init__, add it to the registry
                submod_name = "{0}.{1}".format(module,module_name)
                module_names.append(submod_name)
    #Once everything is imported, the metaclass will register them automatically
    modules = map(import_module, module_names)
    return modules

def find_in_registry(category = None, namespace = None, name = None):
    """
    Find a given category/namespace/name combination in the registry
    category - string, see utils.inputs.registrycategories
    namespace - module namespace, see settings.NAMESPACE
    name - lowercase name of module
    """
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

#initialize the registry
import_task_modules()
