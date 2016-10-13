import os
import unittest

import F1toExcavatorMapper.CSVOperations as csvops
from F1toExcavatorMapper.Constant import Excavator
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class CSVTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file_path = os.path.join(THIS_DIR, 'testdata.csv')

    def __create_individual_file(self):
        target_type = TargetCSVType.individual
        csvops.create_file(self.test_file_path, target_type)

    def __create_family_file(self):
        target_type = TargetCSVType.family
        csvops.create_file(self.test_file_path, target_type)

    def test_file_does_not_exist(self):
        self.assertFalse(csvops.check_file_exists(self.test_file_path))

    def test_created_file_exists(self):
        self.__create_individual_file()
        self.assertTrue(csvops.check_file_exists(self.test_file_path))

    def test_created_individual_file_has_correct_headers(self):
        self.__create_individual_file()
        self.assertTrue(csvops.check_headers_match(self.test_file_path, TargetCSVType.individual))

    def test_created_family_file_has_correct_headers(self):
        self.__create_family_file()
        self.assertTrue(csvops.check_headers_match(self.test_file_path, TargetCSVType.family))

    def test_created_file_has_no_additional_headers(self):
        csvops.create_file(self.test_file_path, TargetCSVType.individual)
        self.assertEqual(len(Excavator.individual_csv_headers), csvops.get_header_count(self.test_file_path))

    def tearDown(self):
        try:
            os.remove(self.test_file_path)
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()
