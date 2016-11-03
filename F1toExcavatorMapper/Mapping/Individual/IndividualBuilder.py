import re

from pandas import Series
import pandas as pd
import F1toExcavatorMapper.Utils.CSVOperations as csvops
import numpy as np

from F1toExcavatorMapper.Mapping import Mapper
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType

regex = re.compile('[^a-zA-Z]')


def add_attributes_to_frame(attribute_data, individual_file_path):
    existing_individual_data = csvops.read_file_without_check(individual_file_path, Mapper.get_index_of_header(TargetCSVType.INDIVIDUAL, SourceCSVType.ATTRIBUTES))
    # By manually indexing we keep the column *and* get the index
    existing_individual_data.index = existing_individual_data.set_index(['PersonId'])

    # Convert to DateTime
    attribute_data['start_date'] = pd.to_datetime(attribute_data['start_date'])
    # Convert to Int
    attribute_data['individual_id_1'] = attribute_data['individual_id_1'].astype(int)
    existing_individual_data['PersonId'] = existing_individual_data['PersonId'].astype(int)
    # Remove duplicates and take the most recent
    attribute_data = attribute_data.groupby(['individual_id_1', 'attribute_name']).max()['start_date'].reset_index()
    # Pivot to get columns of attribute names with values below
    attribute_data = attribute_data.pivot(index='individual_id_1', columns='attribute_name', values='start_date')
    # Change index to PersonId so we can concat
    attribute_data.index.rename('PersonId', True)
    # Result is attributes appended to the existing Individual_Id data
    result = existing_individual_data.join(attribute_data, on='PersonId')
    return result


def build_individual_core_frame(data):
    # Select the subset of columns needed for mapping
    individual_frame = data.loc[:,
                       ['Household_Id', 'Household_Name', 'First_Record', 'Individual_ID', 'First_Name', 'Goes_By',
                        'Middle_Name', 'Last_Name', 'Suffix', 'Marital_Status', 'Mobile_Phone', 'Work_Phone',
                        'Unsubscribed', 'Gender', 'DOB', 'Title', 'Prefix', 'Household_Position', 'Status',
                        'Status_Group', 'Preferred_Email', 'Personal_Email', 'InFellowship_Email']]
    # Rename columns to match Excavator naming
    individual_frame = individual_frame.rename(columns={'Household_Id': 'FamilyId', 'Household_Name': 'FamilyName',
                                                        'First_Record': 'CreatedDate', 'Individual_ID': 'PersonId',
                                                        'First_Name': 'FirstName', 'Last_Name': 'LastName',
                                                        'Marital_Status': 'MaritalStatus',
                                                        'Mobile_Phone': 'MobilePhone',
                                                        'Work_Phone': 'WorkPhone', 'DOB': 'DateOfBirth',
                                                        'Household_Position': 'FamilyRole',
                                                        'Status': 'ConnectionStatus', 'Status_Group': 'RecordStatus',
                                                        'InFellowship_Email': 'Email', 'Goes_By': 'NickName',
                                                        'Middle_Name': 'MiddleName'})
    # Add blank columns that are required
    individual_frame = pd.concat([individual_frame, pd.DataFrame(columns=('HomePhone', 'SMS Allowed?', 'School',
                                                                          'GraduationDate',
                                                                          'AnniversaryDate',
                                                                          'GeneralNote',
                                                                          'MedicalNote',
                                                                          'SecurityNote', 'IsDeceased', 'IsEmailActive',
                                                                          'Allow Bulk Email?'))])
    # Fill default values and apply mapping functions
    individual_frame['SMS Allowed?'] = individual_frame['SMS Allowed?'].fillna('Yes')
    individual_frame['Prefix'] = individual_frame.apply(get_prefix, axis=1)
    individual_frame['FamilyRole'] = individual_frame['FamilyRole'].map(get_household_position)
    individual_frame['IsDeceased'] = individual_frame.apply(get_is_deceased, axis=1)
    individual_frame['RecordStatus'] = individual_frame['RecordStatus'].map(get_record_status)
    individual_frame['Email'] = individual_frame.apply(get_email, axis=1)
    individual_frame['IsEmailActive'] = individual_frame['Unsubscribed'].map(is_email_active)
    individual_frame['Allow Bulk Email?'] = individual_frame['IsEmailActive']
    #
    # # Drop blank id rows
    # individual_frame = individual_frame[np.isfinite(individual_frame['PersonId'])]
    # individual_frame = individual_frame[np.isfinite(individual_frame['FamilyId'])]

    # Ensure that IDs are ints not floats
    individual_frame['PersonId'] = individual_frame['PersonId'].astype(int)
    individual_frame['FamilyId'] = individual_frame['FamilyId'].astype(int)

    # Reorder columns and select only the ones needed by Excavator
    individual_frame = individual_frame[list(TargetCSVType.INDIVIDUAL.columns)]
    return individual_frame


def get_prefix(row):
    prefix = row['Prefix']
    title = row['Title']
    if not title:
        return title
    else:
        return prefix


def get_household_position(value):
    if value == 'Child':
        return value
    else:
        return 'Adult'


def get_record_status(value):
    if value == 'Inactive' or value == 'Deceased' or value == 'System':
        return 'Inactive'
    else:
        return 'Active'


def get_is_deceased(row):
    value = row['RecordStatus']
    if value == 'Deceased':
        return 'Yes'
    else:
        return 'No'


def get_email(row):
    infellowship_email = row['Email']
    personal_email = row['Personal_Email']
    preferred_email = row['Preferred_Email']
    if infellowship_email is not None and infellowship_email != '':
        return infellowship_email
    elif preferred_email is not None and preferred_email != '':
        return preferred_email
    else:
        return personal_email


def is_email_active(value):
    if value is not None and value == 'Yes':
        return 'No'
    else:
        return 'Yes'
