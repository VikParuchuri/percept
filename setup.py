from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "percept-proto",
    version = "0.1",
    packages=['percept-proto', 'percept-proto.data', 'percept-proto.inputs', 'percept-proto.settings'],
    package_data = {
        '': ['*.txt', '*.rst', '*.p', '*.zip'],
        },
    author = "Vik Paruchuri",
    author_email = "vik@equirio.com",
    description = "Platform for generic machine learning tasks.",
    license = "AGPL",
    keywords = "ml machine learning nlp ai algorithm",
    url = "https://github.com/equirio/percept-proto",
    include_package_data = True,
    )