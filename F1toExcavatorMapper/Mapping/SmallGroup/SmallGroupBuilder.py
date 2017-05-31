import re
from urllib.parse import parse_qs

import pandas as pd

from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType
from F1toExcavatorMapper.Utils.Singleton import Singleton

regex = re.compile('[^a-zA-Z]')
ext_regex = re.compile('[e|E]xt[.]*\s*')


failing_concat_ids = set()

group_id = 141679

@Singleton
class SmallGroupBuilder:
    def __init__(self):
        self.attendance_frame = None

    def map(self, data, source_type):
        if source_type == SourceCSVType.SMALL_GROUP:
            return self.build_attendance_frame(data)

    def build_attendance_frame(self, data):
        # Select the subset of columns needed for mapping
        attendance_frame = data.loc[:,
                           ['Individual ID', 'Ministry', 'Activity', 'Roster', 'Date', 'Time', 'Individual Type',
                            'Job', 'Group Type Name', 'Group Name']]

        # Ensure that IDs are ints not floats
        attendance_frame = attendance_frame[pd.notnull(attendance_frame['Individual ID'])]
        attendance_frame['Individual ID'] = attendance_frame['Individual ID'].astype(int)
        # Ensure other critical columns have the correct type

        #Filter
        attendance_frame = attendance_frame[pd.notnull(attendance_frame['Group Name'])]
        attendance_frame = attendance_frame[(attendance_frame['Group Type Name'] == 'Community Groups') |
                                            (attendance_frame['Group Type Name'] == 'TCE Groups')]

        attendance_frame['Ministry'] = attendance_frame['Ministry'].astype(str)
        attendance_frame['Activity'] = attendance_frame['Activity'].astype(str)
        attendance_frame['Roster'] = attendance_frame['Roster'].astype(str)
        attendance_frame['Ministry'] = attendance_frame['Ministry'].map(self.remove_single_quotes)
        attendance_frame['Activity'] = attendance_frame['Activity'].map(self.remove_single_quotes)
        attendance_frame['Roster'] = attendance_frame['Roster'].map(self.remove_single_quotes)
        attendance_frame['Individual Type'] = attendance_frame['Individual Type'].astype(str)

        # Remove nans
        attendance_frame = attendance_frame.fillna('')
        attendance_frame['GroupId'] = group_id

        # Ensure no fancy dynamic date time conversion occurs, so we can do that manually later
        attendance_frame['Date'] = attendance_frame['Date'].astype(str)
        attendance_frame['Time'] = attendance_frame['Time'].astype(str)

        attendance_frame = attendance_frame[list(TargetCSVType.ATTENDANCE.columns)]

        return attendance_frame


    @staticmethod
    def remove_single_quotes(value):
        return value.replace("'", "")

