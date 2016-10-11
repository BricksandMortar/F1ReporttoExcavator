import os
import unittest
import f1toexcavatormap.Mapper as mapper

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class CSVTests(unittest.TestCase):
    def setUp(self):
        self.test_file_path = os.path.join(THIS_DIR, 'testdata.csv')
        try:
            os.remove(self.test_file_path)
        except Exception:
            pass

    # File will have been removed by setUp
    def test_file_does_not_exist(self):
        self.assertFalse(mapper.check_file_exists(self.test_file_path))

    def test_create_file_exists(self):
        mapper.touch("testdata.csv")
        self.assertTrue(mapper.check_file_exists(self.test_file_path))

    # def test_create_file_has_headers(self):

if __name__ == '__main__':
    unittest.main()
