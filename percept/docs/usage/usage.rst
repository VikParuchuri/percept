==================================
Usage
==================================

Percept can be used either programatically, or via the command line.

Command line
---------------------------------

These should all be run from the directory where percept was cloned.  If you installed via pip, substitute `percept-admin.py` for `python manage.py` .

Run automated tests::

    $ python manage.py test --pythonpath=`pwd` --settings=tests.test_settings

Run a workflow::

    $ python manage.py run_flow tests/workflow_config/test_save.conf --pythonpath=`pwd` --settings=tests.test_settings

List available tasks::

    $ python manage.py list_tasks --pythonpath=`pwd` --settings=tests.test_settings

Guides
-----------------------------------

#. `Predicting the NFL Season with Percept <http://vikparuchuri.com/blog/predicting-season-records-for-nfl-teams-part-2/>`_

Examples
-----------------------------------

#. `NFL Season <https://github.com/equirio/nfl_season/>`_
#. `Political Analyzer <https://github.com/VikParuchuri/political-positions/>`_
#. `Evolve your own music <https://github.com/VikParuchuri/evolve-music/>`_
#. `Simpsons character analysis <https://github.com/VikParuchuri/simpsons-scripts/>`_


