import re

import numpy as np
import pandas as pd
import F1toExcavatorMapper.Utils.CSVOperations as csvops

from F1toExcavatorMapper.Utils.Singleton import Singleton
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType

regex = re.compile('[^a-zA-Z]')
ext_regex = re.compile('[e|E]xt[.]*\s*')


@Singleton
class IndividualBuilder:
    def __init__(self):
        self.individual_frame = None

    def map(self, data, source_type):
        if source_type == SourceCSVType.ATTRIBUTES:
            return self.add_attributes_to_frame(data)
        elif source_type == SourceCSVType.REQUIREMENTS:
            return self.add_requirements_to_frame(data)
        else:
            return self.build_individual_core_frame(data)

    def add_requirements_to_frame(self, requirements_data):
        if self.individual_frame is None:
            raise Exception('Individual frame not constructed before individual attributes')

        # By manually indexing we keep the column *and* get the index
        self.individual_frame.index = self.individual_frame.set_index(['PersonId'])

        requirements_data['Date'] = pd.to_datetime(requirements_data['Date'])
        requirements_data['Individual Id'] = requirements_data['Individual Id'].astype(int)

        # Take a copy so we can pivot a second time for the status data
        requirements_data_status = requirements_data.copy(True)

        # Remove duplicates, take the most recent, and pivot to get columns of Requirements with the date as a value
        requirements_data = requirements_data.groupby(['Individual Id', 'Name']).max()['Date'].reset_index()
        requirements_data = requirements_data.pivot(index='Individual Id', columns='Name', values='Date')

        # Rename Name to Name Date and drop entirely empty columns
        for name in requirements_data.columns:
            if requirements_data[name].isnull().all():
                requirements_data.drop(name, axis=1, inplace=True)
            else:
                requirements_data.rename(columns={name: name + ' Date'}, inplace=True)

        # Rename index to be able to concat and then concat
        requirements_data.index.rename('PersonId', True)
        self.individual_frame = self.individual_frame.join(requirements_data, on='PersonId')

        requirements_data_status = requirements_data_status.pivot(index='Individual Id', columns='Name',
                                                                  values='Status')

        # Get rid of blank columns
        for name in requirements_data_status.columns:
            if requirements_data_status[name].isnull().all():
                requirements_data_status.drop(name, axis=1, inplace=True)

        requirements_data_status.index.rename('PersonId', True)
        self.individual_frame = self.individual_frame.join(requirements_data_status, on='PersonId')
        return self.individual_frame

    def add_attributes_to_frame(self, attribute_data):
        if self.individual_frame is None:
            raise Exception('Individual frame not constructed before individual attributes')
        # By manually indexing we keep the column *and* get the index
        self.individual_frame.index = self.individual_frame.set_index(['PersonId'])
        # Convert to DateTime
        attribute_data['start_date'] = pd.to_datetime(attribute_data['start_date'])
        # Convert to Int
        attribute_data['individual_id_1'] = attribute_data['individual_id_1'].astype(int)

        # Check if both start date, end date, and comments are non-consistent, if so we'll copy over booleans.
        consistent = (not attribute_data['start_date'].isnull().values.any()) or \
                     (not attribute_data['comment'].isnull().values.any()) or \
                     (not attribute_data['end_date'].isnull().values.any())

        if not consistent:
            attribute_data_boolean = attribute_data.copy(True)
            attribute_data_boolean = attribute_data_boolean.pivot(index='individual_id_1', columns='attribute_name', values='individual_id_1')
            attribute_data_boolean.index.rename('PersonId', True)

            for name in attribute_data_boolean.columns:
                attribute_data_boolean[name].loc[attribute_data_boolean.index] = True

            self.individual_frame = self.individual_frame.join(attribute_data_boolean, on='PersonId')

        # Take a copy so we can join the comments back on later
        attribute_data_comments = attribute_data.copy(True)
        # Remove duplicates and take the most recent
        attribute_data = attribute_data.groupby(['individual_id_1', 'attribute_name']).max()['start_date'].reset_index()
        # Pivot to get columns of attribute names with values below
        attribute_data = attribute_data.pivot(index='individual_id_1', columns='attribute_name', values='start_date')
        # Rename attribute_name to attribute_name_date and drop empty columns
        for name in attribute_data.columns:
            if attribute_data[name].isnull().all():
                attribute_data.drop(name, axis=1, inplace=True)
            else:
             attribute_data.rename(columns={name: name + ' Date'}, inplace=True)
        # Change index to PersonId so we can concat
        attribute_data.index.rename('PersonId', True)
        # Result is attributes appended to the existing Individual_Id data
        self.individual_frame = self.individual_frame.join(attribute_data, on='PersonId')

        # Also copy the comments over
        attribute_data_comments = attribute_data_comments.pivot(index='individual_id_1', columns='attribute_name',
                                                                values='comment')
        attribute_data_comments.index.rename('PersonId', True)

        for name in attribute_data_comments.columns:
            if attribute_data_comments[name].isnull().all():
                attribute_data_comments.drop(name, axis=1, inplace=True)
            elif not consistent:
                attribute_data.rename(columns={name: name + ' Comment'}, inplace=True)

        self.individual_frame = self.individual_frame.join(attribute_data_comments, on='PersonId')
        return self.individual_frame

    def build_individual_core_frame(self, data):

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
                                                            'Status': 'ConnectionStatus',
                                                            'Status_Group': 'RecordStatus',
                                                            'InFellowship_Email': 'Email', 'Goes_By': 'NickName',
                                                            'Middle_Name': 'MiddleName'})
        # Add blank columns that are required
        individual_frame = pd.concat([individual_frame, pd.DataFrame(columns=('HomePhone', 'SMS Allowed?', 'School',
                                                                              'GraduationDate',
                                                                              'AnniversaryDate',
                                                                              'GeneralNote',
                                                                              'MedicalNote',
                                                                              'SecurityNote', 'IsDeceased',
                                                                              'IsEmailActive',
                                                                              'Allow Bulk Email?'))])

        # Ensure phone numbers are strings and there is no "nan" for blank cells
        individual_frame['HomePhone'] = individual_frame['HomePhone'].astype(str)
        individual_frame['MobilePhone'] = individual_frame['MobilePhone'].astype(str)
        individual_frame['WorkPhone'] = individual_frame['WorkPhone'].astype(str)
        individual_frame['HomePhone'] = individual_frame['HomePhone'].replace('nan', '', regex=True)
        individual_frame['MobilePhone'] = individual_frame['MobilePhone'].replace('nan', '', regex=True)
        individual_frame['WorkPhone'] = individual_frame['WorkPhone'].replace('nan', '', regex=True)

        # Fill default values and apply mapping functions
        individual_frame['SMS Allowed?'] = individual_frame['SMS Allowed?'].fillna('Yes')
        individual_frame['Prefix'] = individual_frame.apply(self.get_prefix, axis=1)
        individual_frame['FamilyRole'] = individual_frame['FamilyRole'].map(self.get_household_position)
        individual_frame['IsDeceased'] = individual_frame.apply(self.get_is_deceased, axis=1)
        individual_frame['RecordStatus'] = individual_frame['RecordStatus'].map(self.get_record_status)
        individual_frame['HomePhone'] = individual_frame['HomePhone'].map(self.cleanup_numbers)
        individual_frame['WorkPhone'] = individual_frame['WorkPhone'].map(self.cleanup_numbers)
        individual_frame['MobilePhone'] = individual_frame['MobilePhone'].map(self.cleanup_numbers)
        individual_frame['Email'] = individual_frame.apply(self.get_email, axis=1)
        individual_frame['IsEmailActive'] = individual_frame['Unsubscribed'].map(self.is_email_active)
        individual_frame['Allow Bulk Email?'] = individual_frame['IsEmailActive']
        individual_frame['DateOfBirth'] = individual_frame['DateOfBirth'].map(csvops.parse_date)
        individual_frame['CreatedDate'] = individual_frame['CreatedDate'].map(csvops.parse_date)

        # Ensure we have a family and PersonId
        individual_frame = individual_frame[pd.notnull(individual_frame['PersonId'])]
        individual_frame = individual_frame[pd.notnull(individual_frame['FamilyId'])]

        # Ensure that IDs are ints not floats
        individual_frame['PersonId'] = individual_frame['PersonId'].astype(int)
        individual_frame['FamilyId'] = individual_frame['FamilyId'].astype(int)
        individual_frame['DateOfBirth'] = pd.to_datetime(individual_frame['DateOfBirth'])

        # Reorder columns and select only the ones needed by Excavator
        individual_frame = individual_frame[list(TargetCSVType.INDIVIDUAL.columns)]
        self.individual_frame = individual_frame
        return individual_frame

    @staticmethod
    def get_prefix(row):
        prefix = row['Prefix']
        title = row['Title']
        if not title:
            return title
        else:
            return prefix

    @staticmethod
    def get_household_position(value):
        if value == 'Child':
            return value
        else:
            return 'Adult'

    @staticmethod
    def get_record_status(value):
        if value == 'Inactive' or value == 'Deceased' or value == 'System':
            return 'Inactive'
        else:
            return 'Active'

    @staticmethod
    def cleanup_numbers(value):
        value = value.translate({ord(c): None for c in '{}[]().'})
        value = ext_regex.sub("x", value)
        # remove all whitespace
        value = "".join(value.split())

        country_index = value.find('+')
        if value.find('x') > 0:
            ext_index = value.find('x')
        else:
            ext_index = len(value)

        if country_index > 0 and (country_index + 3 > len(value) or ext_index - 3 < 0 or
                                              ext_index - 3 > len(value)-country_index-3):
            return ''

        if ext_index > 0 and (ext_index > len(value)):
            return ''

        return value

    @staticmethod
    def get_is_deceased(row):
        value = row['RecordStatus']
        if value == 'Deceased':
            return 'Yes'
        else:
            return 'No'

    @staticmethod
    def get_email(row):
        infellowship_email = row['Email']
        personal_email = row['Personal_Email']
        preferred_email = row['Preferred_Email']
        if not pd.isnull(infellowship_email):
            return infellowship_email
        elif not pd.isnull(preferred_email):
            return preferred_email
        elif not pd.isnull(personal_email):
            return personal_email

    @staticmethod
    def is_email_active(value):
        if value is not None and value == 'Yes':
            return 'No'
        else:
            return 'Yes'
