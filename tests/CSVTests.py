import os
import unittest
import f1toexcavatormap.CSVOperations as csvops
from f1toexcavatormap import Final

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
        self.assertFalse(csvops.check_file_exists(self.test_file_path))

    def created_file_exists(self):
        csvops.create_file(self.test_file_path, Final.individual_headers)
        self.assertTrue(csvops.check_file_exists(self.test_file_path))

    def created_file_has_correct_headers(self):
        csvops.create_file(self.test_file_path, Final.individual_headers)
        self.assertTrue(csvops.check_headers_match(self.test_file_path))

    def created_file_has_no_additional_headers(self):
        csvops.create_file(self.test_file_path, Final.individual_headers)
        self.assertEqual(len(Final.individual_headers), csvops.get_header_count(self.test_file_path))

if __name__ == '__main__':
    unittest.main()
