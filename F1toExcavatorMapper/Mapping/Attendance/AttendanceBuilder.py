import re

import pandas as pd

import F1toExcavatorMapper.Utils.CSVOperations as csvops
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType
from F1toExcavatorMapper.Utils.Singleton import Singleton

regex = re.compile('[^a-zA-Z]')
ext_regex = re.compile('[e|E]xt[.]*\s*')


@Singleton
class AttendanceBuilder:
    def __init__(self):
        self.attendance_frame = None

    def map(self, data, source_type):
        if source_type == SourceCSVType.ATTENDANCE:
            return self.build_attendance_frame(data)
        elif source_type == SourceCSVType.GROUP_MEMBER:
            return self.match_group_member_data(data)

    def match_group_member_data(self, group_member_data):
        if self.attendance_frame is None:
            raise Exception('Attendance frame not constructed before attempting to add group member data')
        # By manually indexing we keep the column *and* get the index
        # self.attendance_frame.index = self.attendance_frame.set_index(['Individual Id', 'Ministry', 'Activity',
        #                                                                'Roster'])
        # self.attendance_frame.index = self.attendance_frame.set_index(['Individual Id'])

        # Convert to Int
        group_member_data['Individual ID'] = group_member_data['Individual ID'].astype(int)
        group_member_data = group_member_data.rename(columns={'Individual ID': 'Individual Id'})

        group_member_data = group_member_data.loc[:, ['Individual Id', 'Ministry', 'Activity', 'Roster', 'Group Id',
                                                      'Group Type Id']]

        # Change index to PersonId so we can concat
        # group_member_data.index = group_member_data.set_index('Individual Id')
        # Replace NaNs
        group_member_data = group_member_data.fillna('')

        print(group_member_data.head())

        # Result is attributes appended to the existing Individual_Id data
        self.attendance_frame = pd.merge(self.attendance_frame, group_member_data, how='outer',
                                         on=['Individual Id', 'Ministry',
                                             'Activity', 'Roster'])
        return self.attendance_frame

    def build_attendance_frame(self, data):

        # Select the subset of columns needed for mapping
        attendance_frame = data.loc[:,
                           ['Individual ID', 'Ministry', 'Activity', 'Roster', 'Date', 'Time', 'Individual Type',
                            'Job']]

        # Rename individual id to match Excavator naming
        attendance_frame = attendance_frame.rename(columns={'Individual ID': 'Individual Id'})

        # Ensure we have a family and PersonId
        attendance_frame = attendance_frame[pd.notnull(attendance_frame['Individual Id'])]

        # Ensure that IDs are ints not floats
        attendance_frame['Individual Id'] = attendance_frame['Individual Id'].astype(int)

        # Ensure no fancy dynamic date time conversion occurs, so we can do that manually later
        attendance_frame['Date'] = attendance_frame['Date'].astype(str)
        attendance_frame['Time'] = attendance_frame['Time'].astype(str)
        attendance_frame = attendance_frame.fillna('')

        self.attendance_frame = attendance_frame
        return attendance_frame
