import decimal
import unittest
import os

import numpy as np
import numpy.testing as npt
import pandas as pd
from pandas import Timestamp

import F1toExcavatorMapper.Utils.CSVOperations as csvops
from F1toExcavatorMapper.Mapping.Finances.FinancialBuilder import FinancialBuilder
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType

TEST_DATA_FILENAME = "/testdata/X1050_Giving.csv"

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class FinancialBuilderTests(unittest.TestCase):
    def setUp(self):
        self.fb = FinancialBuilder.Instance()

    def test_number_of_batches_equals_number_of_group_by_batch_name_date(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        ids_size = batch_data['BatchID'].values.size
        # This seems weird but does work bizarrely
        group_by_size = batch_data.groupby(['BatchName', 'BatchDate']).size().size
        self.assertEqual(ids_size, group_by_size)

    def test_batches_ids_are_all_ints(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        self.assertTrue(batch_data['BatchID'].dtype == int)

    def test_all_batches_have_names(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        self.assertFalse(pd.isnull(batch_data['BatchName']).any())

    def test_batches_all_have_amounts(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        self.assertFalse(pd.isnull(batch_data['BatchAmount']).any())

    def test_batch_dates_are_all_timestamps(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        self.assertTrue(batch_data['BatchDate'].dtype == Timestamp)

    def test_batch_amounts_are_all_decimal(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        self.assertTrue(batch_data['BatchAmount'].dtype == decimal.Decimal)

    def test_batch_ids_are_all_unique(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        unique_ids_size = batch_data['BatchID'].value_counts(dropna=True).size
        ids_size = batch_data['BatchID'].values.size
        self.assertEqual(ids_size, unique_ids_size)

    def test_sum_data_amounts_equal_sum_batch_amounts(self):
        pass

    def test_batch_columns_match(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_data = self.fb.map(df, None)
        npt.assert_array_equal(batch_data.columns.values, TargetCSVType.BATCH.columns)

    # Contribution Tests

    def test_all_contributions_have_funds(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        self.assertFalse(pd.isnull(contributions_data['FundName']).any())

    def test_all_contributions_received_dates_are_dates(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        self.assertTrue(contributions_data['ReceivedDate'].dtype == Timestamp)

    def test_all_check_contributions_have_check_number(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        check_contributions = contributions_data.loc[contributions_data['ContributionTypeName'] == 'Check']
        self.assertFalse(pd.isnull(check_contributions['CheckNumber']).any())

    def test_contributions_amount_equals_contribution_amount(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        self.assertEqual(contributions_data['Amount'].sum(), 6084.99)

    def test_all_contribution_batch_ids_have_batches(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        npt.assert_array_equal(contributions_data['ContributionBatchID'].unique(), self.fb.batch_data['Id'])

    def test_contributions_ids_are_ints(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        contribution_id_is_int = contributions_data['ContributionID'].dtype == int
        contribution_batch_id_is_int = contributions_data['ContributionBatchID'].dtype == int
        contribution_individual_id_is_int = contributions_data['IndividualID'].dtype == int
        self.assertTrue(contribution_id_is_int and contribution_batch_id_is_int and contribution_individual_id_is_int)

    def test_all_contribution_ids_are_unique(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        unique_ids_size = contributions_data['ContributionID'].value_counts(dropna=True).size
        ids_size = contributions_data['ContributionID'].values.size
        self.assertEqual(ids_size, unique_ids_size)

    def test_contributions_columns_match(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        npt.assert_array_equal(contributions_data.columns.values, TargetCSVType.CONTRIBUTION.columns)

    def test_number_of_contributions(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        contributions_data = self.fb.build_contributions(df)
        self.assertEquals(len(contributions_data.index), 36)

    # Shared Data Tests
    def test_batch_shared_data_contains_correct_number_of_batches(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        unique_size = self.fb.batch_data['Id'].value_counts(dropna=True).size
        self.assertEqual(unique_size, 5)

    def test_batch_shared_data_columns_are_all_populated(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        self.assertFalse(self.fb.batch_data.isnull().values.any())

    def test_batch_shared_data_columns_are_correct_types(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        self.fb.map(df, None)
        batch_date_is_date = self.fb.batch_data['Batch_Date'].dtype == Timestamp
        batch_id_is_int = self.fb.batch_data['Id'].dtype == np.int64 or self.fb.batch_data['Id'].dtype == int
        types_correct = batch_date_is_date and batch_id_is_int
        self.assertTrue(types_correct)

    def test_number_of_shared_batch_data_equals_number_of_contributions_group_by_batch_name_date(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        cloned_df = df.copy()
        cloned_df = self.fb.fill_missing_batch_data(cloned_df)
        self.fb.map(df, None)
        ids_size = self.fb.batch_data['Id'].values.size
        # This seems weird but does work bizarrely
        group_by_size = cloned_df.groupby(['Batch_Name', 'Batch_Date']).size().size
        self.assertEqual(ids_size, group_by_size)

    def test_strip_amount_negative(self):
        self.assertEqual(-15.00, self.fb.strip_amount('-$15.00'))

    def test_strip_amount_positive(self):
        self.assertEqual(15.00, self.fb.strip_amount('$15.00'))


if __name__ == '__main__':
    unittest.main()
