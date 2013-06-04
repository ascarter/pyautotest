# -*- coding: utf-8 -*-

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

packages = [ 'pyautotest' ]
requires = [ 'watchdog>=0.6.0' ]
scripts = [ 'bin/autotest' ]

setup(
	name='pyautotest',
	version='0.1.0',
	description='Autotest Python unittest modules',
	long_description=open('README.rst').read(),
	author='Andrew Carter',
	author_email='andrew@ascarter.net',
	url='http://github.com/ascarter/pyautotest',
	scripts=scripts,
	packages=packages,
	package_dir={ 'pyautotest': 'pyautotest' },
	install_requires=requires,
	license=read('LICENSE'),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Operating System :: Unix',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Testing'
	]
)
