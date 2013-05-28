import logging
import unittest
import pyautotest
import subprocess
from watchdog.events import FileSystemMovedEvent, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
from mock import MagicMock, patch
from pyautotest.observers import ChangeHandler

TEST_RESULTS = {
	'OK': """
....
----------------------------------------------------------------------
Ran 4 tests in 0.234s

OK
""",
	'OK_WITH_SKIPPED': """
.s..
----------------------------------------------------------------------
Ran 4 tests in 0.456s

OK (skipped=1)
""",
	'FAILED': """
.FF.
----------------------------------------------------------------------
Ran 4 tests in 0.012s

FAILED (failures=2)
""",
	'FAILED_WITH_SKIPPED': """
.FFs
----------------------------------------------------------------------
Ran 4 tests in 0.012s

FAILED (failures=2, skipped=1)
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
	
	def test_create_handler(self):
		self.assertEqual(self.handler.project_name, 'pyautotest')
	
	def test_file_moved(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['OK'])
			self.handler.run_tests = MagicMock(name='run_tests')
			event = FileSystemMovedEvent(self.src_path, self.dest_path, False)
			self.handler.on_any_event(event)
			self.handler.run_tests.assert_called_with('project/file.py moved')

	def test_file_modified(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['OK'])
			self.handler.run_tests = MagicMock(name='run_tests')
			event = FileModifiedEvent(self.src_path)
			self.handler.on_any_event(event)
			self.handler.run_tests.assert_called_with('project/file.py modified')

	def test_file_created(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['OK'])
			self.handler.run_tests = MagicMock(name='run_tests')
			event = FileCreatedEvent(self.src_path)
			self.handler.on_any_event(event)
			self.handler.run_tests.assert_called_with('project/file.py created')
		
	def test_file_deleted(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['OK'])
			self.handler.run_tests = MagicMock(name='run_tests')
			event = FileDeletedEvent(self.src_path)
			self.handler.on_any_event(event)
			self.handler.run_tests.assert_called_with('project/file.py deleted')
	
	def test_run_ok(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['OK'])
			self.handler.run_tests(reason=__name__)
			subtitle = 'OK 4 tests, 100.0%'
			self.notifier.notify.assert_called_with(self.title, subtitle, __name__, group=self.title)

	def test_run_ok_with_skipped(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['OK_WITH_SKIPPED'])
			self.handler.run_tests(reason=__name__)
			subtitle = 'OK 4 tests, 1 skipped, 100.0%'
			self.notifier.notify.assert_called_with(self.title, subtitle, __name__, group=self.title)
	
	def test_run_failed(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['FAILED'])
			self.handler.run_tests(reason=__name__)
			subtitle = 'FAILED 4 tests, 2 failures, 50.0%'
			self.notifier.notify.assert_called_with(self.title, subtitle, __name__, group=self.title)
		
	def test_run_failed_with_skipped(self):
		with patch('subprocess.Popen') as mock:
			instance = mock.return_value
			instance.communicate.return_value = ('output', TEST_RESULTS['FAILED_WITH_SKIPPED'])
			self.handler.run_tests(reason=__name__)
			subtitle = 'FAILED 4 tests, 2 failures, 1 skipped, 33.3%'
			self.notifier.notify.assert_called_with(self.title, subtitle, __name__, group=self.title)

if __name__ == '__main__':
	unittest.main()
