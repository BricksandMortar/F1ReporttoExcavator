import os
import unittest

import F1toExcavatorMapper.Utils.CSVOperations as csvops
from F1toExcavatorMapper.Mapping.Mapper import get_index_of_header
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class CSVTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file_path = os.path.join(THIS_DIR, 'testdata.csv')

    def __create_individual_file(self):
        target_type = TargetCSVType.INDIVIDUAL
        csvops.create_file(self.test_file_path, target_type)

    def __create_family_file(self):
        target_type = TargetCSVType.FAMILY
        csvops.create_file(self.test_file_path, target_type)

    def test_file_does_not_exist(self):
        self.assertFalse(csvops.check_file_exists(self.test_file_path))

    def test_created_file_exists(self):
        self.__create_individual_file()
        self.assertTrue(csvops.check_file_exists(self.test_file_path))

    def test_created_individual_file_has_correct_headers(self):
        self.__create_individual_file()
        self.assertTrue(csvops.check_headers_match(self.test_file_path, TargetCSVType.INDIVIDUAL))

    def test_created_family_file_has_correct_headers(self):
        self.__create_family_file()
        self.assertTrue(csvops.check_headers_match(self.test_file_path, TargetCSVType.FAMILY))

    def test_created_file_has_no_additional_headers(self):
        csvops.create_file(self.test_file_path, TargetCSVType.INDIVIDUAL)
        self.assertEqual(len(TargetCSVType.INDIVIDUAL.columns), csvops.get_header_count(self.test_file_path))

    def test_file_delete(self):
        csvops.create_file(self.test_file_path, TargetCSVType.INDIVIDUAL)
        csvops.delete_file(self.test_file_path)
        self.assertFalse(csvops.check_file_exists(self.test_file_path))

    def tearDown(self):
        try:
            os.remove(self.test_file_path)
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()
