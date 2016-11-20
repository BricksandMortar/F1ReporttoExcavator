import math
from decimal import Decimal
from re import sub

import pandas as pd
import numpy as np

from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType
from F1toExcavatorMapper.Utils.Singleton import Singleton
import F1toExcavatorMapper.Utils.CSVOperations as csvops


@Singleton
class FinancialBuilder:
    def __init__(self):
        self.batch_data = None
        self.batch_data_dict = None

    def map(self, data, source_type):
        if self.batch_data is not None:
            return self.build_batches()
        else:
            return self.build_contributions(data)

    def build_batches(self):
        batch_data = self.batch_data.copy()
        batch_data = batch_data.rename(columns={'Id': 'BatchID', 'Batch_Name': 'BatchName', 'Batch_Date': 'BatchDate',
                                                'Batch_Entered': 'BatchAmount'})
        batch_data['BatchDate'] = batch_data['BatchDate'].map(csvops.parse_date)
        batch_data['BatchAmount'] = batch_data['BatchAmount'].map(self.strip_amount)
        batch_data = batch_data[list(TargetCSVType.BATCH.columns)]
        return batch_data

    def build_contributions(self, data):

        self.build_shared_batch_data(data)

        # Select the subset of columns needed for mapping
        data = data.loc[:,
               ['Contributor_ID', 'Contributor_Type', 'Fund', 'SubFund_Code', 'Received_Date', 'Reference', 'Memo',
                'Type', 'Amount', 'True_Value', 'Transaction_ID', 'Batch_Entered', 'Batch_Name',
                'Batch_Date']]

        # Rename columns to Excavator naming
        contributions_data = data.rename(columns={'Contributor_ID': 'IndividualID', 'Fund': 'FundName',
                                                  'SubFund_Code': 'SubFundName', 'Received_Date': 'ReceivedDate',
                                                  'Type': 'ContributionTypeName', 'Transaction_ID': 'ContributionID', 'Contributor_Type': 'ContributorType'})
        # Add blank columns to be filled by data created with logic
        # Add blank columns that are required
        contributions_data = pd.concat(
            [contributions_data, pd.DataFrame(columns=(
                'FundIsActive', 'SubFundIsActive', 'CheckNumber', 'StatedValue', 'FundGLAccount', 'SubFundGLAccount',
                'ContributionBatchID', 'ConcatId'))])

        # Get ContributionBatchId from shared batch id
        contributions_data['ConcatId'] = contributions_data.apply(self.get_concat_id, axis=1)

        # Map complex columns
        contributions_data['ContributionBatchID'] = contributions_data.apply(self.get_batch_number, axis=1)
        contributions_data['FundIsActive'] = contributions_data['FundIsActive'].fillna('Yes')
        contributions_data['SubFundIsActive'] = contributions_data['SubFundIsActive'].fillna('Yes')
        contributions_data['Amount'] = contributions_data['Amount'].map(self.strip_amount)
        contributions_data['CheckNumber'] = contributions_data.apply(self.get_check_number, axis=1)
        contributions_data['StatedValue'] = contributions_data.apply(self.get_stated_value, axis=1)

        # Cleanup data
        contributions_data = contributions_data.dropna(
            subset=['ContributionID', 'IndividualID', 'ContributionBatchID', 'Amount'])

        # Set correct types
        contributions_data['ContributionID'] = contributions_data['ContributionID'].astype(int)
        contributions_data['IndividualID'] = contributions_data['IndividualID'].astype(int)
        contributions_data['ContributionBatchID'] = contributions_data['ContributionBatchID'].astype(int)
        contributions_data['Amount'] = contributions_data['Amount'].astype(float)
        contributions_data['StatedValue'] = contributions_data['StatedValue'].astype(float)
        contributions_data['ReceivedDate'] = contributions_data['ReceivedDate'].map(csvops.parse_date)

        # Ensure the columns are in the correct order
        contributions_data = contributions_data[list(TargetCSVType.CONTRIBUTION.columns)]
        return contributions_data

    def build_shared_batch_data(self, data):
        # Create shared batch data
        unique_batches = data.copy()
        # Get a concat id
        unique_batches['ConcatId'] = unique_batches['Batch_Date'].map(str) + unique_batches['Batch_Name'] + \
                                     unique_batches['Batch_Entered']
        unique_batches = unique_batches[['Batch_Name', 'Batch_Date', 'ConcatId', 'Batch_Entered']]
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

    @staticmethod
    def strip_amount(value):
        return Decimal(sub(r'[^\d.]', '', value))

    @staticmethod
    def get_check_number(row):
        contribution_type = row['ContributionTypeName']
        if contribution_type == 'Check':
            reference = row['Reference']
            if reference != '':
                return int(reference)
            return 0
        return np.nan

    @staticmethod
    def get_stated_value(row):
        amount = row['Amount']
        true_value = row['True_Value']
        if true_value is None or true_value == '' or math.isnan(true_value):
            return Decimal(amount)
        return Decimal(true_value)

    @staticmethod
    def get_concat_id(row):
        return row['Batch_Date'] + row['Batch_Name'] + row['Batch_Entered']

    def get_batch_number(self, row):
        concat_id = row['ConcatId']
        return self.batch_data_dict.get(concat_id)
