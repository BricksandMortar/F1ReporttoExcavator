import os
import unittest

import pandas as pd

import F1toExcavatorMapper.Utils.CSVOperations as csvops

from F1toExcavatorMapper.Mapping.AttributeNotes.AttributeNotesBuilder import AttributeNotesBuilder
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType

TEST_DATA_FILENAME = "/testdata/A2501E_AttributesToNotes.csv"
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class AttributeNotesBuilderTests(unittest.TestCase):
    def setUp(self):
        self.anb = AttributeNotesBuilder.Instance()

    def test_ids_are_unique(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        attribute_notes = self.anb.map(df, SourceCSVType.ATTRIBUTE_NOTES)
        unique_ids_size = attribute_notes['note_id'].value_counts(dropna=True).size
        ids_size = attribute_notes['note_id'].values.size
        self.assertEqual(ids_size, unique_ids_size)

    def test_data_is_not_null(self):
        df = csvops.read_file_without_check(THIS_DIR + TEST_DATA_FILENAME)
        attribute_notes = self.anb.map(df, SourceCSVType.ATTRIBUTE_NOTES)
        self.assertFalse(pd.isnull(attribute_notes['individual_id_1']).any() and pd.isnull(
            attribute_notes['attribute_group_name'].any()) and pd.isnull(
            attribute_notes['attribute_name']) and pd.isnull(attribute_notes['comment']).any())


if __name__ == '__main__':
    unittest.main()
