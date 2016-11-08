import unittest
import os
import F1toExcavatorMapper.Utils.CSVOperations as csvops
from F1toExcavatorMapper.Mapping.Finances.FinancialBuilder import FinancialBuilder
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class FinancialBuilderTests(unittest.TestCase):
    def setUp(self):
        self.fb = FinancialBuilder.Instance()

    def test_number_of_batches_equals_number_of_group_by_batch_name_date(self):
        pass

    def test_batches_all_have_unique_ids(self):
        pass

    def test_batches_ids_are_all_ints(self):
        pass

    def test_all_batches_have_names(self):
        pass

    def test_batches_all_have_amounts(self):
        pass

    def test_batch_amounts_are_all_decimal(self):
        pass

    def test_batch_ids_are_all_unique(self):
        pass

    def test_sum_data_amounts_equal_sum_batch_amounts(self):
        pass

    def test_batch_columns_match(self):
        pass

    def test_all_contributions_have_funds(self):
        pass

    def test_all_contributions_have_gls(self):
        pass

    def test_all_contributions_have_an_active_value(self):
        pass

    def test_all_contributions_received_dates_are_dates(self):
        pass

    def test_all_check_contributions_have_check_number(self):
        pass

    def test_contributions_amount_equals_contribution_amount(self):
        pass

    def test_all_contribution_batch_ids_have_batches(self):
        pass

    def test_all_contribution_ids_are_unique(self):
        pass

    def test_contributions_columns_match(self):
        pass

    # Shared Data Tests
    def test_batch_shared_data_contains_correct_number_of_batches(self):
        df = csvops.read_file_without_check(THIS_DIR + "\\testdata\\X1050_Giving.csv")
        self.fb.map(df, None)
        ids = self.fb.batch_data['Id']
        unique_values = ids.value_counts(dropna=True)
        unique_size = unique_values.size
        self.assertEqual(unique_size, 4)

    def test_batch_shared_data_columns_are_all_populated(self):
        pass

    def test_batch_shared_data_columns_are_correct_types(self):
        pass

if __name__ == '__main__':
    unittest.main()
