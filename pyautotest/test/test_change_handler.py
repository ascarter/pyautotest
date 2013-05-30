import logging
import os
import unittest
import pyautotest
import subprocess
from watchdog.events import FileSystemMovedEvent, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
from mock import MagicMock, patch
from pyautotest.observers import ChangeHandler

TEST_RESULTS_OK = {
	'label': 'OK 4 tests, 100.0%',
	'output': """
....
----------------------------------------------------------------------
Ran 4 tests in 0.234s

OK
"""
}

TEST_RESULTS_OK_WITH_SKIPPED = {
	'label': 'OK 4 tests, 1 skipped, 100.0%',
	'output': """
.s..
----------------------------------------------------------------------
Ran 4 tests in 0.456s

OK (skipped=1)
"""
}

TEST_RESULTS_FAILED = {
	'label': 'FAILED 4 tests, 2 failures, 50.0%',
	'output': """
.FF.
----------------------------------------------------------------------
Ran 4 tests in 0.012s

FAILED (failures=2)
"""
}

TEST_RESULTS_FAILED_WITH_SKIPPED = {
	'label': 'FAILED 4 tests, 2 failures, 1 skipped, 33.3%',
	'output': """
.FFs
----------------------------------------------------------------------
Ran 4 tests in 0.012s

FAILED (failures=2, skipped=1)
"""
}

TEST_RESULTS_FAILED_WITH_ERRORS = {
	'label': 'FAILED 4 tests, 2 errors, 50.0%',
	'output': """
.EE.
----------------------------------------------------------------------
Ran 4 tests in 0.012s

FAILED (errors=2)
"""
}

TEST_RESULTS_FAILED_WITH_ERRORS_AND_SKIPPED = {
	'label': 'FAILED 4 tests, 1 error, 1 skipped, 66.7%',
	'output': """
.Es.
----------------------------------------------------------------------
Ran 4 tests in 0.012s

FAILED (errors=1, skipped=1)
"""
}

TEST_RESULTS_FAILED_WITH_FAILURES_ERRORS_AND_SKIPPED = {
	'label': 'FAILED 4 tests, 1 failure, 1 error, 1 skipped, 33.3%',
	'output': """
.EsF
----------------------------------------------------------------------
Ran 4 tests in 0.012s

FAILED (failures=1, errors=1, skipped=1)
"""
}


class ChangeHandlerTestCase(unittest.TestCase):
	def setUp(self):
		logging.disable(logging.CRITICAL)
		self.maxDiff = None
		self.src_path = './project/file.py'
		self.dest_path = './project2/file2.py'
		self.title = 'pyautotest unit tests'
		self.handler = ChangeHandler()
		self.notifier = self.handler.notifier
		self.notifier.notify = MagicMock(name='notify')
		
	def tearDown(self):
		logging.disable(logging.INFO)
	
	def _run_event(self, event):
		self.handler.run_tests = MagicMock(name='run_tests')
		self.handler.on_any_event(event)
		src_path = os.path.relpath(event.src_path)
		self.handler.run_tests.assert_called_with('{0} {1}'.format(src_path, event.event_type))
	
	def _run_test(self, result):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', result['output'])
			self.handler.run_tests(reason=__name__)
			self.notifier.notify.assert_called_with(self.title, result['label'], __name__, group=self.title)
		
	def test_create_handler(self):
		self.assertEqual(self.handler.project_name, 'pyautotest')
	
	def test_file_moved(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS_OK)
			event = FileSystemMovedEvent(self.src_path, self.dest_path, False)
			self._run_event(event)

	def test_file_modified(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS_OK)
			event = FileModifiedEvent(self.src_path)
			self._run_event(event)

	def test_file_created(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS_OK)
			event = FileCreatedEvent(self.src_path)
			self._run_event(event)
		
	def test_file_deleted(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS_OK)
			event = FileDeletedEvent(self.src_path)
			self._run_event(event)
	
	def test_run_ok(self):
		self._run_test(TEST_RESULTS_OK)

	def test_run_ok_with_skipped(self):
		self._run_test(TEST_RESULTS_OK_WITH_SKIPPED)
	
	def test_run_failed(self):
		self._run_test(TEST_RESULTS_FAILED)
		
	def test_run_failed_with_skipped(self):
		self._run_test(TEST_RESULTS_FAILED_WITH_SKIPPED)
	
	def test_run_failed_with_errors(self):
		self._run_test(TEST_RESULTS_FAILED_WITH_ERRORS)
	
	def test_run_failed_with_errors_and_skipped(self):
		self._run_test(TEST_RESULTS_FAILED_WITH_ERRORS_AND_SKIPPED)
	
	def test_run_failed_with_failures_and_errors_and_skipped(self):
		self._run_test(TEST_RESULTS_FAILED_WITH_FAILURES_ERRORS_AND_SKIPPED)

if __name__ == '__main__':
	unittest.main()
