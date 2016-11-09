import math
from re import sub

import pandas as pd
from decimal import Decimal

from F1toExcavatorMapper.Utils.Singleton import Singleton


@Singleton
class FinancialBuilder:
    def __init__(self):
        self.batch_data = None
        self.batch_data_dict = None

    def map(self, data, source_type):
        if self.batch_data is not None:
            self.build_batches(data)
        else:
            self.build_contributions(data)

    def build_batches(self, data):
        # data['start_date'] = pd.to_datetime(data['start_date'])
        # # Convert to Int
        # attribute_data['individual_id_1'] = attribute_data['individual_id_1'].astype(int)
        # self.individual_frame['PersonId'] = self.individual_frame['PersonId'].astype(int)
        # # Remove duplicates and take the most recent
        # attribute_data = attribute_data.groupby(['individual_id_1', 'attribute_name']).max()['start_date'].reset_index()
        # # Pivot to get columns of attribute names with values below
        # attribute_data = attribute_data.pivot(index='individual_id_1', columns='attribute_name', values='start_date')
        # # Change index to PersonId so we can concat
        # attribute_data.index.rename('PersonId', True)
        # # Result is attributes appended to the existing Individual_Id data
        # self.individual_frame = self.individual_frame.join(attribute_data, on='PersonId')
        # return self.batch_data
        pass

    def build_contributions(self, data):
        # Select the subset of columns needed for mapping
        data = data.loc[:,
               ['Contributor_ID', 'Fund', 'SubFund_Code', 'Received_Date', 'Reference', 'Memo',
                'Type', 'Amount', 'True_Value', 'Transaction_ID', 'Batch_Entered', 'Batch_Name',
                'Batch_Date']]

        # Create shared batch data
        unique_batches = data.copy()
        # Get a concat id
        unique_batches['ConcatId'] = unique_batches['Batch_Date'].map(str) + unique_batches['Batch_Name']
        unique_batches = unique_batches[['Batch_Name', 'Batch_Date', 'ConcatId']]
        # Generate ids
        id_values = pd.factorize(unique_batches['ConcatId'])[0]
        # Get ids starting at 1
        id_values += 1
        unique_batches['Id'] = pd.Series(id_values)
        unique_batches = unique_batches.dropna()
        unique_batches['Batch_Name'] = unique_batches['Batch_Name'].apply(str)
        unique_batches['Id'] = unique_batches['Id'].apply(int)
        self.batch_data = unique_batches.drop_duplicates()
        # Generate a dict to map more easily from
        self.batch_data_dict = pd.Series(unique_batches.Id.values, index=unique_batches.ConcatId).to_dict()

        # Rename columns to Excavator naming
        contributions_data = data.rename(columns={'Contributor_ID': 'IndividualID', 'Fund': 'FundName',
                                                  'SubFund_Code': 'SubFundName', 'Received_Date': 'ReceivedDate',
                                                  'Type': 'ContributionTypeName', 'Transaction_ID': 'ContributionID'})
        # Add blank columns to be filled by data created with logic
        # Add blank columns that are required
        contributions_data = pd.concat(
            [contributions_data, pd.DataFrame(columns=(
                'SubFundIsActive', 'CheckNumber', 'StatedValue', 'FundGLAccount', 'SubFundGLAccount',
                'ContributionBatchID'))])

        # Get ContributionBatchId from shared batch id
        contributions_data['ConcatId'] = contributions_data['Batch_Date'].map(str) + unique_batches['Batch_Name']
        contributions_data['ContributionBatchID'] = contributions_data['ConcatId'].map(self.batch_data_dict)

        # Map complex columns
        contributions_data['SubFundIsActive'] = contributions_data['SubFundIsActive'].fillna('Yes')
        contributions_data['Amount'] = contributions_data['Amount'].map(self.strip_amount)
        contributions_data['CheckNumber'] = contributions_data.apply(self.get_check_number, axis=1)
        contributions_data['StatedValue'] = contributions_data.apply(self.get_stated_value, axis=1)

        # Cleanup data
        contributions_data = contributions_data.dropna(subset=['ContributionID', 'IndividualID', 'ContributionBatchID', 'FundName', 'Amount'])
        # Set correct types
        contributions_data['ContributionID'] = contributions_data['ContributionID'].astype(int)
        contributions_data['IndividualID'] = contributions_data['IndividualID'].astype(int)
        contributions_data['ContributionBatchID'] = contributions_data['ContributionBatchID'].astype(int)
        contributions_data['CheckNumber'] = contributions_data['CheckNumber'].astype(int)
        contributions_data['Amount'] = contributions_data['Amount'].astype(float)
        contributions_data['StatedValue'] = contributions_data['StatedValue'].astype(float)

        from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType
        contributions_data = contributions_data[list(TargetCSVType.CONTRIBUTIONS.columns)]
        print(contributions_data)
        return contributions_data

    @staticmethod
    def strip_amount(value):
        return Decimal(sub(r'[^\d.]', '', value))

    @staticmethod
    def get_check_number(row):
        contribution_type = row['ContributionTypeName']
        if contribution_type == 'Check':
            return row['Reference']
        return ''

    @staticmethod
    def get_stated_value(row):
        amount = row['Amount']
        true_value = row['True_Value']
        if true_value is None or true_value == '' or math.isnan(true_value):
            return Decimal(amount)
        return Decimal(true_value)
