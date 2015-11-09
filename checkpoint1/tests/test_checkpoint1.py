import unittest
import os
from checkpoint1.amity import Admin


class CheckPoint1Test(unittest.TestCase):

    def setUp(self):
        """ this setUp method makes the Admin class available to all test methods """
            self.file_path = os.path.dirname(os.path.abspath(__file__))
            self.data_file = os.path.join(self.file_path, "data")
        self.admin = Admin()

    def test_get_data(self):
        """ test the getdata(iterator, file) method from the admin class that it returns true """
        output_file = os.path.join(self.data_file, "output.txt")
        self.result = self.admin.getData(2, output_file)
        self.assertIsInstance(self.result, dict)

    def test_get_rooms(self):
        """ test the getdata(iterator, file) method from the admin class that it returns true """
        self.result = self.admin.getRooms()
        self.assertIsInstance(self.result, dict)

    def test_for_check_allocations(self):
        """ this tests the checkAllocations method in Admin class """
        self.result = self.admin.checkAllocations()
        self.assertIsInstance(self.result, list)

    def test_for_read_from_output_file(self):
        """ tests for readFromOutputFile method """
        self.output = self.admin.readFromOutputFile()
        self.assertIsInstance(self.output, dict)

    """
		tests for readFromOutputFile method 
	"""

    def test_for_return_room_members(self):
        self.result = self.admin.returnRoomMembers("nigeria")
        self.assertIsInstance(self.result, list)


if __name__ == '__main__':
    unittest.main()
