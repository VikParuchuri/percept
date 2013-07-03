from setuptools import setup, find_packages
import os

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join)
    in a platform-neutral way.  From django.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

packages = []
package_data = {}

percept_dir = 'percept'
for dirpath, dirnames, filenames in os.walk(percept_dir):
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    parts = fullsplit(dirpath)
    package_name = '.'.join(parts)
    if '__init__.py' in filenames:
        packages.append(package_name)
    elif filenames:
        relative_path = []
        while '.'.join(parts) not in packages:
            relative_path.append(parts.pop())
        relative_path.reverse()
        path = os.path.join(*relative_path)
        package_files = package_data.setdefault('.'.join(parts), [])
        package_files.extend([os.path.join(path, f) for f in filenames])

with open('requirements.txt') as f:
    required = f.read().splitlines()

print packages
print package_data

setup(
    name = "percept",
    version = "0.1",
    author = "Equirio",
    author_email = "vik@equirio.com",
    description = "Platform for generic machine learning tasks.",
    license = "AGPL",
    keywords = "ml machine learning nlp ai algorithm",
    url = "https://github.com/equirio/percept",
    include_package_data = True,
    packages=packages,
    package_data=package_data,
    scripts=['percept/bin/percept-admin.py'],
    )