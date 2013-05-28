import unittest
from pyautotest import observers

class ObserversTestCase(unittest.TestCase):
	def setUp(self):
		self.maxDiff = None
	
	def tearDown(self):
		pass
	
	# @unittest.skip("Not working")
	def test_notify(self):
		self.assertTrue(True)
	
# 	def test_notify_fail(self):
# 		self.assertTrue(False)

if __name__ == '__main__':
	unittest.main()
