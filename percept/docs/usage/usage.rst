==================================
Usage
==================================

Percept can be used either programatically, or via the command line.

Command line
---------------------------------

Run automated tests::

    $ python manage.py test --pythonpath=`pwd` --settings=tests.test_settings

Run a workflow::

    $ python manage.py run_flow tests/workflow_config/test_save.conf --pythonpath=`pwd` --settings=tests.test_settings

List available tasks::

    $ python manage.py list_tasks --pythonpath=`pwd` --settings=tests.test_settings