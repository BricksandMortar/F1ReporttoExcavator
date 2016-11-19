import os
import unittest

import datetime

import F1toExcavatorMapper.Utils.CSVOperations as csvops
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType
import numpy.testing as npt

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

    def test_read_attribute_data_has_correct_columns(self):
        df = csvops.read_file_without_check(THIS_DIR+'/testdata/A2501E_ConnectionStepsAttributes.csv')
        npt.assert_array_equal(df.columns.values, SourceCSVType.ATTRIBUTES.columns)

    def test_read_individual_household_has_correct_columns(self):
        df = csvops.read_file_without_check(THIS_DIR+'/testdata/X9400_no_attributes.csv')
        npt.assert_array_equal(df.columns.values, SourceCSVType.INDIVIDUAL_HOUSEHOLD.columns)

    def test_date_parse_mddyy(self):
        correct_date = datetime.date(1957, 2, 23)
        self.assertEqual(correct_date, csvops.parse_date("2/23/57"))

    def test_date_parse_mmddyy(self):
        correct_date = datetime.date(1957, 2, 23)
        self.assertEqual(correct_date, csvops.parse_date("02/23/57"))

    def test_date_parse_mmddyyyy(self):
        correct_date = datetime.date(2001, 12, 31)
        self.assertEqual(correct_date, csvops.parse_date("12/31/2001"))

    def tearDown(self):
        try:
            os.remove(self.test_file_path)
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()
