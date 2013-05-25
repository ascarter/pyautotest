# -*- coding: utf-8 -*-

import logging
import os
import time
from watchdog.observers import Observer
from unitwatch.observers import Notifier, ChangeHandler

# Configure logging
logging.basicConfig(format='%(asctime)s (%(name)s) [%(levelname)s]: %(message)s',
	datefmt='%m-%d-%Y %H:%M:%S',
	level=logging.INFO)
logger = logging.getLogger('unitwatch')

def main():
	while True:
		event_handler = ChangeHandler()
		event_handler.run_tests()
		observer = Observer()
		observer.schedule(event_handler, os.getcwd(), recursive=True)
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()

if __name__ == "__main__":
	main()