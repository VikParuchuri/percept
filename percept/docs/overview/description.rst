===============================================
Description
===============================================

Percept is a modular, extensible framework for machine learning that emphasizes easy testing and deployability.

There are several important concepts to the percept framework:

#. Settings
#. Workflows
#. Tasks
#. Inputs
#. Formatters


Settings
-------------------------------------

Settings define global attributes, such as what type of caching to use for task values, and where to store results.

Workflows
-------------------------------------

Workflows are high level constructs that tie together multiple tasks.  A workflow could take you from data in a database to predicted clusters, for example.

A workflow, when it finishes running, will optionally allow you to store its results.  It will also allow you to go into an ipython shell and manipulate and visualize the results when it is done running.  Workflows can also be reloaded and used for prediction.

What tasks a workflow ties together, and what data it needs to load are pulled from a configuration file.  Workflows can be run from the command line, or programatically.

Tasks
--------------------------------------

Tasks are discrete units of work.  One task may load sound files, and another may turn them into feature vectors, for instance.  A task can perform any work.

Tasks have the following features:
#. Tasks can define which variables they would like to persist.  These variables are stored by the cache specified in the settings.
#. Tasks can also define a tester class, which will be used to run tests on the tasks.
#. Tasks have a namespace, category, and name, which can be used to search for them in the registry later.
#. Tasks can define dependencies, which are executed and provided to the task before it runs.
#. Tasks can have both a training method and a prediction method.  One can be used to train the classifier or feature extractor, and the other used to perform the same operation on new data.
#. Tasks can be executed by themselves, or with a workflow.

Inputs
-------------------------------------

Inputs read data in, and pass it to a formatter class.  The data can be from a database, csv file, json file, etc.  Each input defines what kind of values it will read in.

Formatters
-------------------------------------

Formatters reformat input data into data that a task can use.  Formatters define what they convert from (defined by the input class), and what they convert to (defined by the task class).  When a workflow runs, it will inspect its tasks to determine what type of data they accept.  It will then pull the data in using an appropriate input and find the right formatter to convert it.

