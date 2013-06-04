pyautotest
==========

This is a utility to provide continuous testing during development. It watches for changes in source and test files and will run the test suite when a change is detected.

Additionally, pyautotest supports posting notifications on Mac OS X using Notification Center and libnotify on Linux.

Install
-------

*Pip*:

	pip install pyautotest

*Source*:

	python setup.py install


How to Use
----------

A utility is created `autotest` that can be run at the root of your Python project. It will use unittest's discover feature to find tests. It will watch for any `*.py` files from the current directory recursively::

	usage: autotest [-h] [-l L]

	Continuously run unit tests when changes detected

	optional arguments:
	  -h, --help           show this help message and exit
	  -l L, --log-level L  set logger level


Optionally, you can run directly from Python using the following::

	python -m pyautotest.cli


Dependencies
------------

*Required*:

* watchdog - https://pypi.python.org/pypi/watchdog/0.6.0

*Optional*:

* mock - https://pypi.python.org/pypi/mock
* terminal-notifier - https://github.com/alloy/terminal-notifier
