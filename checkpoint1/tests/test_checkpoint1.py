import unittest
from checkpoint1.amity import Admin


class CheckPoint1Test(unittest.TestCase):
	"""
		this setUp method makes the Admin class available to all test methods
	"""
	def setUp(self):
		self.admin = Admin()

	"""
		test the getdata(iterator, file) method from the admin class that it returns true
	"""
	def testGetData(self):
		self.result = self.admin.getData( 2, "../data/output.txt")
		self.assertIsInstance(self.result, dict)

	"""
		test the getdata(iterator, file) method from the admin class that it returns true
	"""
	def testGetRooms(self):
		self.result = self.admin.getRooms()
		self.assertIsInstance(self.result, dict)


	"""
		this tests the checkAllocations method in Admin class
	"""
	def test_for_checkAllocations(self):
		self.result = self.admin.checkAllocations()
		self.assertIsInstance(self.result, list)

	"""
		tests for readFromOutputFile method 
	"""
	def test_for_readFromOutputFile(self):
		self.output = self.admin.readFromOutputFile()
		self.assertIsInstance(self.output, dict)

	"""
		tests for readFromOutputFile method 
	"""
	def test_for_returnRoomMembers(self):
		self.result = self.admin.returnRoomMembers("nigeria")
		self.assertIsInstance(self.result, list)


if __name__ == '__main__':
    unittest.main()