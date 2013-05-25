# -*- coding: utf-8 -*-

import datetime
import logging
import os
import platform
import subprocess
import sys
import time
import types

from distutils.spawn import find_executable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger('unitwatch')

class Notifier(object):
	def __init__(self):
		self.notifier = None
		
		if platform.system() == 'Darwin':
			expanded_path = os.environ['PATH'] + os.pathsep + "/Applications/terminal-notifier.app/Contents/MacOS"
			self.notifier = find_executable("terminal-notifier", path=expanded_path)			
			def _get_args(self, title, subtitle, info_text, sound, group, open_url):
				args = []
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
			self.notifier = find_executable("notify-send")
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
			subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
class ChangeHandler(FileSystemEventHandler):
	"""Public: React to changes in source tree and run unit tests
	"""
	
	def __init__(self):
		self.notifier = Notifier()
	
	def _get_now(self):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	def _getext(self, filename):
		return os.path.splitext(filename)[-1].lower()
		
	def on_any_event(self, event):
		if event.is_directory:
			return
		if self._getext(event.src_path) == '.py':
			self.run_tests()
	
	def run_tests(self):
		"""Private: Run unit tests with unittest
		"""
		
		logger.info("Running unit tests at {}".format(self._get_now()))
		cmd = "python -m unittest discover -b"
		proc = subprocess.Popen(["python", "-m", "unittest", "discover"], stderr=subprocess.PIPE)
		proc_out, proc_err = proc.communicate()
		print(proc_err)
		results = proc_err.splitlines()
		result = "Failed" if proc.returncode else "Passed"
		subtitle = results[-1]
		info_text = results[-3]
		if self.notifier:
			self.notifier.notify("Unit Tests", subtitle, info_text, group="unitwatch")
