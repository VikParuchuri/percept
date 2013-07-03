=================================
Installation Overview
=================================

Manual - Recommended
--------------------------------
This assumes that you already have git installed on your computer. The main steps are::

	$ git clone git://github.com/equirio/percept.git
	$ cd percept
	$ xargs -a apt-packages.txt apt-get install
	$ virtualenv /path/to/percept
	$ source /path/to/percept/bin/activate
	$ pip install -r pre-requirements.txt
	$ pip install -r requirements.txt

See :doc:`usage` for usage instructions.

You can skip the virtualenv commands if you like, but they will be a major help in keeping the packages for this repo separate from the rest of your system.

PyPi
----------------------------------

You can find the percept package `here <https://pypi.python.org/pypi/percept/0.1>`_.

Install by doing::

    $ pip install percept

You may need to manually install the requirements afterwards.