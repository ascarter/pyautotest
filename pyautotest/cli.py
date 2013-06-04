# -*- coding: utf-8 -*-

import argparse
import logging
import os
import signal
import time

from watchdog.observers import Observer
from pyautotest.observers import Notifier, ChangeHandler

# Configure logging
logging.basicConfig(format='%(asctime)s (%(name)s) [%(levelname)s]: %(message)s',
	datefmt='%m-%d-%Y %H:%M:%S',
	level=logging.INFO)
logger = logging.getLogger('pyautotest')

def main():
	parser = argparse.ArgumentParser(description="Continuously run unit tests when changes detected")
	parser.add_argument('-l', '--log-level',
		metavar='L',
		default='INFO',
		dest='loglevel',
		action='store',
		help='set logger level')
	args = parser.parse_args()

	# Handle options
	logger.setLevel(getattr(logging, args.loglevel.upper(), None))

	while True:
		event_handler = ChangeHandler()
		event_handler.run_tests()
		observer = Observer()
		observer.schedule(event_handler, os.getcwd(), recursive=True)

		# Avoid child zombie processes
		signal.signal(signal.SIGCHLD, signal.SIG_IGN)
		
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()

if __name__ == "__main__":
	main()