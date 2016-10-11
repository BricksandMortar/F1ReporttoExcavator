import os
import unittest
import f1toexcavatormap.Mapper as mapper

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class CSVTests(unittest.TestCase):
    def setUp(self):
        self.test_file_path = os.path.join(THIS_DIR, 'testdata.csv')
        os.remove(self.test_file_path)

    # File will have been removed by setUp
    def test_file_does_not_exist(self):
        self.assertFalse(mapper.check_file_exists(self.test_file_path))


if __name__ == '__main__':
    unittest.main()
