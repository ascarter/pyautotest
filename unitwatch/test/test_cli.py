import unittest
from unitwatch import cli

class CLITestCase(unittest.TestCase):
	def setUp(self):
		self.maxDiff = None
	
	def tearDown(self):
		pass
	
	def test_main(self):
		self.assertTrue(True)
	
if __name__ == '__main__':
	unittest.main()
