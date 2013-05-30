# -*- coding: utf-8 -*-

import datetime
import logging
import os
import platform
import re
import subprocess
import sys
import time
import types
import unittest

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger('pyautotest')

class Notifier(object):
	def __init__(self):
		self.notifier = None
		
		if platform.system() == 'Darwin':
			self.notifier = "/usr/bin/open"
			def _get_args(self, title, subtitle, info_text, sound, group, open_url):
				args = ["-b", "nl.superalloy.oss.terminal-notifier", "--args"]
				if title:
					args.extend(["-title", '"{}"'.format(title)])
				if subtitle:
					args.extend(["-subtitle", '"{}"'.format(subtitle)])
				if info_text:
					args.extend(["-message", '"{}"'.format(info_text)])
				if group:
					args.extend(["-group", '"{}"'.format(group)])
				if open_url:
					args.extend(["-open", '"{}"'.format(open_url)])
				else:
					args.extend(["-activate", "com.apple.Terminal"])
				return args
			self._get_args = types.MethodType(_get_args, self)
		elif platform.system() == 'Linux':
			self.notifier = 'notify-send'
			def _get_args(self, title, subtitle, info_text, sound, group, open_url):
				args = []
				value = []
				if title:
					args.extend(['"{}"'.format(title)])				
				if subtitle:
					value.append(subtitle)
					args.extend(["-i", "dialog-ok" if subtitle == 'OK' else "dialog-error"])
				if info_text:
					value.append(info_text)
				args.append('"{0}"'.format("<br/>".join(value)))
				return args
			self.get_args = types.MethodType(_get_args, self)
		if not self.notifier:
			logger.warn("Notifications disabled")
	
	def _get_args(self, title, subtitle, info_text, sound, group, open_url):
		return []
	
	def notify(self, title, subtitle, info_text=None, sound=False, group=None, open_url=None):
		if self.notifier:
			cmd = [self.notifier]
			cmd.extend(self._get_args(title, subtitle, info_text, sound, group, open_url))
			logger.debug("Notify command: {0}".format(' '.join(cmd)))
			subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
class ChangeHandler(FileSystemEventHandler):
	"""Public: React to changes in source tree and run unit tests
	"""
	
	def __init__(self):
		self.notifier = Notifier()
		self.project_name = os.path.basename(os.getcwd())
		self.test_total_check = re.compile('^Ran (\\d+) .*$')
		self.test_status_check = re.compile('^(FAILED|OK)')
		self.test_failures_check = re.compile('((failures|skipped|errors)\\=(\\d+))')
			
	def on_any_event(self, event):
		if event.is_directory:
			return
		(filename, ext) = os.path.splitext(event.src_path)
		if ext.lower() == '.py':
			reason = '{0} {1}'.format(os.path.relpath(event.src_path), event.event_type)
			self.run_tests(reason)
		
	def _check_results(self, output, reason):
		if not output:
			return
			
		status = None
		passed = 0
		failed = 0
		errors = 0
		skipped = 0
		total = 0
		percentage = 0
		
		title = "{0} unit tests".format(self.project_name)
		lines = output.splitlines()
		
		matches = self.test_total_check.match(lines[-3])
		if matches:
			total = int(matches.group(1)) if matches.group(1) else 0

		if matches:
			matches = self.test_status_check.match(lines[-1])
			status = matches.group(1)
		
		matches = self.test_failures_check.findall(lines[-1])
		if matches:
			for (m, label, value) in matches:
				if label == 'failures':
					failed = int(value) if value else 0
				if label == 'skipped':
					skipped = int(value) if value else 0
				if label == 'errors':
					errors = int(value) if value else 0
				
		passed = total - failed - errors - skipped
		if total > 0:
			percentage = (float(passed) / float(total - skipped)) * 100.0
		
		subtitle = ""
		if status:
			subtitle += "{0}".format(status)
		if total:
			subtitle += " {0} {1},".format(total, 'tests' if total > 1 else 'test')
		if failed:
			subtitle += " {0} {1},".format(failed, 'failure' if failed == 1 else 'failures')
		if errors:
			subtitle += " {0} {1},".format(errors, 'error' if errors == 1 else 'errors')
		if skipped:
			subtitle += " {0} {1},".format(skipped, 'skipped')
		subtitle += " {0:.1f}%".format(percentage)
		info_text = reason

		logger.info(subtitle)
		if self.notifier:
			self.notifier.notify(title, subtitle, info_text, group=title)
	
	def run_tests(self, reason="Unit test run"):
		"""Private: Run unit tests with unittest discover
		"""
		
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		logger.info("Running unit tests at {0}".format(now))
		if reason:
			logger.info("  {0}".format(reason))
		cmd = ["python", "-m", "unittest", "discover", "--buffer"]
		logger.debug("Exec tests: {0}".format(" ".join(cmd)))
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc_out, proc_err = proc.communicate()
		if proc_out:
			logger.debug(proc_out)
		if proc_err:
			logger.info(proc_err)
		self._check_results(proc_err, reason)
