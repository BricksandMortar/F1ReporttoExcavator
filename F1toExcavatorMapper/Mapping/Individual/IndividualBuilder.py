import re

from pandas import Series
import pandas as pd

from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType

regex = re.compile('[^a-zA-Z]')


def build_individual_frame(data):
    individual_frame = data.loc[:, ['Household_Id', 'Household_Name', 'First_Record', 'Individual_ID', 'First_Name',
                                'Last_Name', 'Suffix', 'Marital_Status', 'Mobile_Phone', 'Work_Phone', 'Unsubscribed',
                                'Gender', 'DOB', 'Title', 'Prefix', 'Household_Position', 'Status', 'Status_Group',
                                    'Preferred_Email', 'Personal_Email']]
    individual_frame = individual_frame.rename(columns={'Household_Id': 'FamilyId', 'Household_Name': 'FamilyName',
                                                'First_Record': 'CreatedDate', 'Individual_ID': 'PersonId',
                                                'First_Name': 'FirstName', 'Last_Name': 'LastName',
                                                'Marital_Status': 'MaritalStatus', 'Mobile_Phone': 'MobilePhone',
                                                'Work_Phone': 'WorkPhone', 'DOB': 'DateOfBirth'})

    individual_frame = pd.concat([individual_frame, pd.DataFrame(columns=('HomePhone', 'SMS Allowed?', 'School',
                                                   'GraduationDate',
                                                   'AnniversaryDate',
                                                   'GeneralNote',
                                                   'MedicalNote',
                                                   'SecurityNote'))])
    individual_frame['SMS Allowed?'] = individual_frame['SMS Allowed?'].fillna('Yes')
    individual_frame['Prefix'] = individual_frame['Prefix'].apply(lambda row: get_prefix(row['Prefix'], row['Title']),
                                                                  axis=1)
    individual_frame = individual_frame[list(TargetCSVType.INDIVIDUAL.columns)]
    return individual_frame


def get_prefix(prefix, title):
    if not title:
        return title
    else:
        return prefix


def get_household_position(value):
    pass


def get_status(value):
    pass


def get_record_status(value):
    pass


def get_is_deceased(value):
    pass


def get_email(value):
    pass

