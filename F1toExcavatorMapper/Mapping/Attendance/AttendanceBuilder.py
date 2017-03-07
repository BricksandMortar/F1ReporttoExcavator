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
        self.attendance_mapping = None
        self.attendance_frame = None

    def map(self, data, source_type):
        if source_type == SourceCSVType.ATTENDANCE:
            return self.build_attendance_frame(data)
        elif source_type == SourceCSVType.ATTENDANCE_MAPPING:
            return self.match_attendance_mapping_data(data)

    def match_attendance_mapping_data(self, attendance_mapping_data):
        attendance_mapping_data = attendance_mapping_data.rename(
            columns={'F1 Ministry': 'Ministry', 'F1 Activity': 'Activity',
                     'F1 Roster': 'Roster'})
        attendance_mapping_data['Ministry'] = attendance_mapping_data['Ministry'].astype(str)
        attendance_mapping_data['Activity'] = attendance_mapping_data['Activity'].astype(str)
        attendance_mapping_data['Roster'] = attendance_mapping_data['Roster'].astype(str)
        attendance_mapping_data['Ministry'] = attendance_mapping_data['Ministry'].map(self.remove_single_quotes)
        attendance_mapping_data['Activity'] = attendance_mapping_data['Activity'].map(self.remove_single_quotes)
        attendance_mapping_data['Roster'] = attendance_mapping_data['Roster'].map(self.remove_single_quotes)
        attendance_mapping_data['Individual Type'] = attendance_mapping_data['Individual Type'].astype(str)

        attendance_mapping_data['IsParticipant'] = attendance_mapping_data.apply(self.is_participant, axis=1)
        attendance_mapping_data['ConcatId'] = attendance_mapping_data.apply(self.get_concat_id, axis=1)
        self.attendance_mapping = pd.Series(attendance_mapping_data['Group Id'].values,
                                            index=attendance_mapping_data.ConcatId).to_dict()
        return None

    def build_attendance_frame(self, data):
        if self.attendance_mapping is None:
            raise Exception('Attendance mapping data not constructed before attempting to add attendance data')
        # Select the subset of columns needed for mapping

        attendance_frame = data.loc[:,
                           ['Individual ID', 'Ministry', 'Activity', 'Roster', 'Date', 'Time', 'Individual Type',
                            'Job']]

        # Ensure that IDs are ints not floats

        attendance_frame = attendance_frame[pd.notnull(attendance_frame['Individual ID'])]
        attendance_frame['Individual ID'] = attendance_frame['Individual ID'].astype(int)
        # Ensure other critical columns have the correct type
        attendance_frame['Ministry'] = attendance_frame['Ministry'].astype(str)
        attendance_frame['Activity'] = attendance_frame['Activity'].astype(str)
        attendance_frame['Roster'] = attendance_frame['Roster'].astype(str)
        attendance_frame['Ministry'] = attendance_frame['Ministry'].map(self.remove_single_quotes)
        attendance_frame['Activity'] = attendance_frame['Activity'].map(self.remove_single_quotes)
        attendance_frame['Roster'] = attendance_frame['Roster'].map(self.remove_single_quotes)
        attendance_frame['Individual Type'] = attendance_frame['Individual Type'].astype(str)

        # Remove nans
        attendance_frame = attendance_frame.fillna('')

        attendance_frame['IsParticipant'] = attendance_frame.apply(self.is_participant, axis=1)
        attendance_frame['ConcatId'] = attendance_frame.apply(self.get_concat_id, axis=1)
        attendance_frame['GroupId'] = attendance_frame.apply(self.get_group_id, axis=1)

        # Ensure no fancy dynamic date time conversion occurs, so we can do that manually later
        attendance_frame['Date'] = attendance_frame['Date'].astype(str)
        attendance_frame['Time'] = attendance_frame['Time'].astype(str)

        attendance_frame = attendance_frame[list(TargetCSVType.ATTENDANCE.columns)]
        return attendance_frame

    @staticmethod
    def is_participant(row):
        if row['Individual Type'] == 'Participant':
            return 'P'
        return ''

    @staticmethod
    def remove_single_quotes(value):
        return value.replace("'", "")

    @staticmethod
    def get_concat_id(row):
        return (row['Ministry'] + row['Activity'] + row['Roster'] + row['IsParticipant']).replace("'", "").replace(' ', '')

    def get_group_id(self, row):
        try:
            return self.attendance_mapping[row['ConcatId']]
        except:
            print(row['ConcatId'])
            return '0'