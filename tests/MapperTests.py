import os
import unittest

import pandas as pd

import F1toExcavatorMapper.Utils.CSVOperations as csvops
from F1toExcavatorMapper.Exception import MappingFileNotFound
from F1toExcavatorMapper.Mapping import Mapper
from F1toExcavatorMapper.Mapping import Mode
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
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

    @staticmethod
    def __create_family_data_frame():
        series_one = {'FamilyId': 1,
                      'FamilyName': 'Test One',
                      'CreatedDate': '2016-01-12',
                      'Campus': 'MAIN',
                      'Address': '',
                      'Address2': '',
                      'City': '',
                      'State': '',
                      'ZipCode': '',
                      'Country': '',
                      'SecondaryAddress': '',
                      'SecondaryAddress2': '',
                      'SecondaryCity': '',
                      'SecondaryState': '',
                      'SecondaryZip': '',
                      'SecondaryCountry': ''}
        series_two = {'FamilyId': 26,
                      'FamilyName': 'Test Two',
                      'CreatedDate': '2016-01-12',
                      'Campus': 'MAIN',
                      'Address': '',
                      'Address2': '',
                      'City': '',
                      'State': '',
                      'ZipCode': '',
                      'Country': '',
                      'SecondaryAddress': '',
                      'SecondaryAddress2': '',
                      'SecondaryCity': '',
                      'SecondaryState': '',
                      'SecondaryZip': '',
                      'SecondaryCountry': ''}
        data_frame = pd.DataFrame([series_one, series_two], columns=TargetCSVType.FAMILY.columns)
        return data_frame

    @staticmethod
    def __create_individual_data_frame():
        series_one = {'FamilyId': 2,
                      'FamilyName': 'Family Name One',
                      'CreatedDate': '2016-01-12',
                      'PersonId': 3,
                      'Prefix': 'Mr.',
                      'FirstName': 'Arran',
                      'NickName': '',
                      'MiddleName': '',
                      'LastName': 'France',
                      'Suffix': '',
                      'FamilyRole': '',
                      'MaritalStatus': '',
                      'ConnectionStatus': '',
                      'RecordStatus': '',
                      'IsDeceased': False,
                      'HomePhone': '',
                      'MobilePhone': '',
                      'WorkPhone': '',
                      'SMS Allowed?': True,
                      'Email': '',
                      'IsEmailActive': True,
                      'Allow Bulk Email?': True,
                      'Gender': 'M',
                      'DateOfBirth': '',
                      'School': '',
                      'GraduationDate': '',
                      'AnniversaryDate': '',
                      'GeneralNote': '',
                      'MedicalNote': '',
                      'SecurityNote': ''}
        series_two = {'FamilyId': 2,
                      'FamilyName': 'Family Name Two',
                      'CreatedDate': '2016-01-12',
                      'PersonId': 3551,
                      'Prefix': 'Mr.',
                      'FirstName': 'Juan',
                      'NickName': '',
                      'MiddleName': '',
                      'LastName': 'Bang',
                      'Suffix': '',
                      'FamilyRole': '',
                      'MaritalStatus': '',
                      'ConnectionStatus': '',
                      'RecordStatus': '',
                      'IsDeceased': True,
                      'HomePhone': '',
                      'MobilePhone': '',
                      'WorkPhone': '',
                      'SMS Allowed?': False,
                      'Email': '',
                      'IsEmailActive': True,
                      'Allow Bulk Email?': True,
                      'Gender': 'Male',
                      'DateOfBirth': '',
                      'School': '',
                      'GraduationDate': '',
                      'AnniversaryDate': '',
                      'GeneralNote': '',
                      'MedicalNote': '',
                      'SecurityNote': ''}
        data_frame = pd.DataFrame([series_one, series_two], columns=TargetCSVType.INDIVIDUAL.columns)
        return data_frame

    def test_get_individual_csv_file_path(self):
        self.assertEqual(Mapper.get_target_file_path(TargetCSVType.INDIVIDUAL, self.test_file_path), THIS_DIR+'\\'+TargetCSVType.INDIVIDUAL.name.lower())

    def test_get_family_csv_file_path(self):
        self.assertEqual(Mapper.get_target_file_path(TargetCSVType.FAMILY, self.test_file_path),
                             THIS_DIR + '\\'+ TargetCSVType.FAMILY.name.lower())

    def test_get_index_of_f1_family_header(self):
        self.assertEqual(Mapper.get_index_of_header(TargetCSVType.FAMILY, SourceCSVType.INDIVIDUAL_HOUSEHOLD), 48)

    def test_get_index_of_f1_individual_header(self):
        self.assertEqual(Mapper.get_index_of_header(TargetCSVType.INDIVIDUAL, SourceCSVType.INDIVIDUAL_HOUSEHOLD), 0)

    def test_get_index_of_f1_attribute_header(self):
        self.assertEqual(Mapper.get_index_of_header(TargetCSVType.INDIVIDUAL, SourceCSVType.ATTRIBUTES), 0)

    def test_set_up_no_source_file_path_exception(self):
        with self.assertRaises(MappingFileNotFound.MappingFileNotFound):
            Mapper.set_up(self.test_file_path, TargetCSVType.INDIVIDUAL, Mode.Mode.APPEND)

    def tearDown(self):
        try:
            os.remove(self.test_file_path)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()
