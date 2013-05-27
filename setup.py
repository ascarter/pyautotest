# -*- coding: utf-8 -*-

from distutils.core import setup

packages = [ 'pyautotest' ]
requires = [ 'watchdog>=0.6.0' ]
scripts  = [ 'bin/autotest' ]
setup(
	name='pyautotest',
	version='1.0',
	description='Autotest Python unittest modules',
	# long_description=open('README.rst').read(),
	author='Andrew Carter',
	author_email='andrew@ascarter.net',
	url='http://github.com/ascarter/pyautotest',
	scripts=scripts,
	packages=packages,
	package_dir={ 'pyautotest': 'pyautotest' },
	install_requires=requires,
	license=open('LICENSE').read(),
	classifiers=(
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: MIT',
		'Programming Language :: Python'
	)
)
