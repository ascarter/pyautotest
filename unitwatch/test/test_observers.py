import unittest
from unitwatch import observers

class CLITestCase(unittest.TestCase):
	def setUp(self):
		self.maxDiff = None
	
	def tearDown(self):
		pass
	
	def test_notify(self):
		self.assertTrue(True)
	
if __name__ == '__main__':
	unittest.main()
