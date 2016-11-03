import unittest
from pandas import Series
import pandas as pd
import numpy.testing as npt
import numpy as np

from F1toExcavatorMapper.Mapping.Family import FamilyBuilder
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType


class FamilyBuilderTests(unittest.TestCase):




    fake_head_individual_household = {'Individual_ID': '77071800',
                                      'Member_Envelope': '',
                                      'Barcode': '',
                                      'Title': '',
                                      'Prefix': 'Mr.',
                                      'First_Name': 'Frederick',
                                      'Goes_By': 'Fred',
                                      'Middle_Name': 'Lucas',
                                      'Last_Name': 'Binks',
                                      'Former_Name': '',
                                      'Suffix': 'Sr.',
                                      'Household_Position': 'Head',
                                      'Gender': 'Male',
                                      'Marital_Status': 'Married',
                                      'Age': '21',
                                      'DOB': '23/12/94',
                                      'Status_Group': 'Attendee',
                                      'Status': 'Core',
                                      'Substatus': '',
                                      'status_date': '',
                                      'Status_Comment': 'Comment here',
                                      'Tag_Comment': 'Shellfish',
                                      'Opt_In_Directory': 'No',
                                      'Unsubscribed': 'No',
                                      'Former_Denomination': '',
                                      'School_Type': '',
                                      'School': '',
                                      'Employer': '',
                                      'Occupation': '',
                                      'Occupation_Desc': '',
                                      'First_Record': '7/17/11',
                                      'Last_Updated': '8/19/16',
                                      'Last_Attended': '8/19/16',
                                      'Last_Activity_Attended': 'Example Activity',
                                      'Last_Roster_Attended': 'Main Service',
                                      'last_contact_date': '6/11/16',
                                      'Last_Gave_On': '8/12/16',
                                      'Last_Gift': '$50.00',
                                      'Preferred_Phone': '',
                                      'Mobile_Phone': '318-648-8319',
                                      'Work_Phone': '318-783-7120',
                                      'Emergency_Phone': 'Anna Binks 318 773-4205',
                                      'Preferred_Email': '',
                                      'InFellowship_Email': 'fred@fakeinbox.com',
                                      'Personal_Email': 'fred@fakeinbox.com',
                                      'Facebook': '',
                                      'Linkedin': '',
                                      'Twitter': '',
                                      'Household_Id': '53330355',
                                      'Household_Name': 'Frederick and Anna Binks',
                                      'HH_First_Name': 'Frederick and Anna',
                                      'HH_Last_Name': 'Binks',
                                      'HH_Preferred_Phone': '318-648-8319',
                                      'HH_Preferred_Email': 'fred@fakeinbox.com',
                                      'HH_Head_Name': 'Frederick Binks',
                                      'HH_Head_DOB': '23/12/94',
                                      'HH_Head_Status': 'Core ',
                                      'HH_Head_SubStatus': '',
                                      'HH_Head_First_Record': '7/17/11',
                                      'HH_Head_Phone': '318-648-8319',
                                      'HH_Head_Email': 'fred@fakeinbox.com',
                                      'HH_Spouse_Name': 'Anna Binks',
                                      'HH_Spouse_DOB': '21/11/95',
                                      'HH_Spouse_Status': 'Core',
                                      'HH_Spouse_SubStatus': '',
                                      'HH_Spouse_First_Record': '7/17/11',
                                      'HH_Spouse_Phone': '318-748-8319',
                                      'HH_Spouse_Email': 'anna@fakeinbox.com',
                                      'HH_Children': '',
                                      'HH_Children_Ages': '',
                                      'HH_Childs_Last_Attendance': '',
                                      'AddressID': '43659945',
                                      'Street_Address': '10721 Holly Springs',
                                      'City': 'Houston',
                                      'State_Province': 'TX',
                                      'Postal_Area': '710',
                                      'Postal_Code_5': '77042',
                                      'Postal_Code': '',
                                      'County': '',
                                      'Country': '',
                                      'Address_Comments': '',
                                      'Verified': '',
                                      'Attribute_Group': '',
                                      'Attribute': '',
                                      'Created_Date': '',
                                      'Start_Date': '',
                                      'End_Date': '',
                                      'Pastor_Staff': '',
                                      'Department': '',
                                      'Comment': ''}

    fake_spouse_individual_household = {'Individual_ID': '77071801',
                                        'Member_Envelope': '',
                                        'Barcode': '',
                                        'Title': '',
                                        'Prefix': 'Mrs.',
                                        'First_Name': 'Anna',
                                        'Goes_By': '',
                                        'Middle_Name': '',
                                        'Last_Name': 'Binks',
                                        'Former_Name': '',
                                        'Suffix': '',
                                        'Household_Position': 'Spouse',
                                        'Gender': 'Female',
                                        'Marital_Status': 'Married',
                                        'Age': '20',
                                        'DOB': '21/11/95',
                                        'Status_Group': 'Attendee',
                                        'Status': 'Core',
                                        'Substatus': '',
                                        'status_date': '',
                                        'Status_Comment': '',
                                        'Tag_Comment': '',
                                        'Opt_In_Directory': 'No',
                                        'Unsubscribed': 'No',
                                        'Former_Denomination': '',
                                        'School_Type': '',
                                        'School': '',
                                        'Employer': '',
                                        'Occupation': '',
                                        'Occupation_Desc': '',
                                        'First_Record': '7/17/11',
                                        'Last_Updated': '8/13/16',
                                        'Last_Attended': '8/19/16',
                                        'Last_Activity_Attended': 'Example Activity',
                                        'Last_Roster_Attended': 'Main Service',
                                        'last_contact_date': '6/11/16',
                                        'Last_Gave_On': '',
                                        'Last_Gift': '',
                                        'Preferred_Phone': '',
                                        'Mobile_Phone': '318-748-8319',
                                        'Work_Phone': '318-785-7120',
                                        'Emergency_Phone': '',
                                        'Preferred_Email': '',
                                        'InFellowship_Email': 'anna@fakeinbox.com',
                                        'Personal_Email': 'anna@fakeinbox.com',
                                        'Facebook': '',
                                        'Linkedin': '',
                                        'Twitter': '',
                                        'Household_Id': '53330355',
                                        'Household_Name': 'Frederick and Anna Binks',
                                        'HH_First_Name': 'Frederick and Anna',
                                        'HH_Last_Name': 'Binks',
                                        'HH_Preferred_Phone': '318-648-8319',
                                        'HH_Preferred_Email': 'fred@fakeinbox.com',
                                        'HH_Head_Name': 'Frederick Binks',
                                        'HH_Head_DOB': '23/12/94',
                                        'HH_Head_Status': 'Core ',
                                        'HH_Head_SubStatus': '',
                                        'HH_Head_First_Record': '7/17/11',
                                        'HH_Head_Phone': '318-648-8319',
                                        'HH_Head_Email': 'fred@fakeinbox.com',
                                        'HH_Spouse_Name': 'Anna Binks',
                                        'HH_Spouse_DOB': '21/11/95',
                                        'HH_Spouse_Status': 'Core',
                                        'HH_Spouse_SubStatus': '',
                                        'HH_Spouse_First_Record': '7/17/11',
                                        'HH_Spouse_Phone': '318-748-8319',
                                        'HH_Spouse_Email': 'anna@fakeinbox.com',
                                        'HH_Children': '',
                                        'HH_Children_Ages': '',
                                        'HH_Childs_Last_Attendance': '',
                                        'AddressID': '43659945',
                                        'Street_Address': '10721 Holly Springs',
                                        'City': 'Houston',
                                        'State_Province': 'TX',
                                        'Postal_Area': '710',
                                        'Postal_Code_5': '77042',
                                        'Postal_Code': '',
                                        'County': '',
                                        'Country': '',
                                        'Address_Comments': '',
                                        'Verified': '',
                                        'Attribute_Group': '',
                                        'Attribute': '',
                                        'Created_Date': '',
                                        'Start_Date': '',
                                        'End_Date': '',
                                        'Pastor_Staff': '',
                                        'Department': '',
                                        'Comment': ''}

    def __get_individual_household_data_frame(self):
        return pd.DataFrame([self.fake_spouse_individual_household, self.fake_head_individual_household],
                            columns=SourceCSVType.INDIVIDUAL_HOUSEHOLD.columns)

    def test_clean_up_state(self):
        test_states = ('tx',
                       'LA',
                       'Tn',
                       'LA.',
                       'AZ',
                       'unknown',
                       'OH',
                       'IL',
                       'AL',
                       'CA',
                       'MS',
                       'VA',
                       'MO',
                       'OK',
                       'GA',
                       '71082',
                       'Co',
                       'NY',
                       'FL',
                       'AR.',
                       '71110',
                       'AE',
                       'IA',
                       'WY',
                       'WA',
                       'LALA',
                       'SC',
                       'MA',
                       'AR',
                       'Louisiana (LA)',
                       'l',
                       'WI',
                       '77619',
                       'KY',
                       'OR',
                       'MI',
                       'AP',
                       'Colorado',
                       'Louisiana',
                       'KS',
                       'UT',
                       'SD',
                       ':A',
                       'ls',
                       'MD',
                       'Tx.',
                       'NM',
                       '????',
                       'LA`',
                       '71129',
                       'HI',
                       '?????',
                       'PA',
                       '71107',
                       'Illinois',
                       '71111',
                       'Missouri',
                       'AK'
                       )
        states = pd.Series(test_states).map(FamilyBuilder.clean_up_state)
        correct_states = pd.Series(('TX',
                                    'LA',
                                    'TN',
                                    'LA',
                                    'AZ',
                                    '',
                                    'OH',
                                    'IL',
                                    'AL',
                                    'CA',
                                    'MS',
                                    'VA',
                                    'MO',
                                    'OK',
                                    'GA',
                                    '',
                                    'CO',
                                    'NY',
                                    'FL',
                                    'AR',
                                    '',
                                    'AE',
                                    'IA',
                                    'WY',
                                    'WA',
                                    '',
                                    'SC',
                                    'MA',
                                    'AR',
                                    '',
                                    '',
                                    'WI',
                                    '',
                                    'KY',
                                    'OR',
                                    'MI',
                                    'AP',
                                    '',
                                    '',
                                    'KS',
                                    'UT',
                                    'SD',
                                    '',
                                    'LS',
                                    'MD',
                                    'TX',
                                    'NM',
                                    '',
                                    'LA',
                                    '',
                                    'HI',
                                    '',
                                    'PA',
                                    '',
                                    '',
                                    '',
                                    '',
                                    'AK'
                                    ))
        npt.assert_array_equal(correct_states, states)

    def test_clean_up_zip(self):
        zips = ('71101',
                '71101',
                '71101',
                '71101',
                '71101',
                '71101',
                '99999',
                '38002',
                '71107',
                '71111',
                '71111',
                '71111',
                '71111',
                '71111',
                '71111',
                '99999',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '11',
                '',
                '',
                '9063',
                '9063',
                '9063',
                '9063',
                '9063',
                '2458',
                '',
                '',
                '',
                '',
                '',
                '',
                '2339',
                '2339',
                '2324',
                '',
                '',
                '',
                '',
                '9643',
                '9643',
                '9643',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '7111',
                '',
                '',
                '',
                '',
                '',
                '',
                '11',
                '7112',
                '',
                '',
                '7111',
                '',
                '',
                '',
                '1950',
                '1950',
                '7106',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '7115',
                '7115',
                '',
                '',
                '',
                '',
                '',
                ''
                )

        correct_zips = ('71101',
                        '71101',
                        '71101',
                        '71101',
                        '71101',
                        '71101',
                        '99999',
                        '38002',
                        '71107',
                        '71111',
                        '71111',
                        '71111',
                        '71111',
                        '71111',
                        '71111',
                        '99999',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        '',
                        ''
                        )
        test_zips = pd.Series(zips).map(FamilyBuilder.clean_up_zip)
        npt.assert_array_equal(correct_zips, test_zips)

    def test_check_build_family_frame_columns(self):
        family_frame = FamilyBuilder.build_family_frame(self.__get_individual_household_data_frame())
        npt.assert_array_equal(family_frame.columns.values, TargetCSVType.FAMILY.columns)

    def test_check_build_family_frame_country(self):
        family_frame = FamilyBuilder.build_family_frame(self.__get_individual_household_data_frame())
        npt.assert_array_equal(family_frame['Country'].unique(), 'US')

    def test_check_build_family_frame_campus(self):
        family_frame = FamilyBuilder.build_family_frame(self.__get_individual_household_data_frame())
        npt.assert_array_equal(family_frame['Campus'].unique(), 'MAIN')

    def test_build_family_frame_duplicate_families(self):
        family_frame = FamilyBuilder.build_family_frame(self.__get_individual_household_data_frame())
        duplicated = family_frame.duplicated(subset='FamilyId')
        self.assertTrue(np.sum(duplicated) == 0)


if __name__ == '__main__':
    unittest.main()
