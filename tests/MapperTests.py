import os
import unittest

import pandas as pd

import F1toExcavatorMapper.Utils.CSVOperations as csvops
from F1toExcavatorMapper.Mapping import Mapper
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

    def test_check_family_existing_ids(self):
        self.__create_family_file()
        data_frame = self.__create_family_data_frame()
        csvops.write_file(self.test_file_path, data_frame)
        self.assertListEqual(Mapper.get_existing_ids(self.test_file_path, TargetCSVType.FAMILY), [1, 26])

    def test_check_individual_existing_ids(self):
        self.__create_individual_file()
        data_frame = self.__create_individual_data_frame()
        csvops.write_file(self.test_file_path, data_frame)
        self.assertListEqual(Mapper.get_existing_ids(self.test_file_path, TargetCSVType.INDIVIDUAL), [3, 3551])

    def tearDown(self):
        try:
            os.remove(self.test_file_path)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()
