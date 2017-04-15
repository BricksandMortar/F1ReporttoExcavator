import re

import pandas as pd

from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType
from F1toExcavatorMapper.Utils.Singleton import Singleton

# This builder takes an attendance mapping file and a set of attendance events and joins them on a concatid which is formed from the job, roster, activity, and ministry attended
# The concatid is matched against a dictionary created from the mapping file. The matching first tries for an exact match, then a match ignoring job, and then finally ignoring roster.


regex = re.compile('[^a-zA-Z]')
ext_regex = re.compile('[e|E]xt[.]*\s*')

# Jobs that require a special mapping rule to be followed
jobs_that_require_a_special_map = {'JH Group Ldr', 'JH Tues 3:30', 'JH Greeter', 'JH Check -in', 'Game',
                                   'JH Band Leader', 'JH Band', 'JH Tech', 'HS Worship', 'Director/Pastor',
                                   'HS Graphics', 'HS Greeter & Follow up', 'HS Group Ldr', 'HS Guest',
                                   'HS Ldrshp Developer', 'HS Leader', 'HS Lighting', 'HS Sound', 'HS Volunteer',
                                   'HS Worship', 'HS Worship Ldr'}

failing_concat_ids = set()


def replace_any(value):
    if value == '-- any --':
        return ''
    else:
        return value


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
                     'F1 Roster': 'Roster', 'F1 Job': 'Job'})
        attendance_mapping_data.fillna('', inplace=True)
        attendance_mapping_data['Ministry'] = attendance_mapping_data['Ministry'].astype(str)
        attendance_mapping_data['Activity'] = attendance_mapping_data['Activity'].astype(str)
        attendance_mapping_data['Roster'] = attendance_mapping_data['Roster'].astype(str)
        attendance_mapping_data['Job'] = attendance_mapping_data['Job'].astype(str)
        attendance_mapping_data['Ministry'] = attendance_mapping_data['Ministry'].map(self.remove_single_quotes)
        attendance_mapping_data['Activity'] = attendance_mapping_data['Activity'].map(self.remove_single_quotes)
        attendance_mapping_data['Roster'] = attendance_mapping_data['Roster'].map(self.remove_single_quotes)
        attendance_mapping_data['Job'] = attendance_mapping_data['Job'].map(self.remove_single_quotes)

        attendance_mapping_data['Individual Type'] = attendance_mapping_data['Individual Type'].astype(str)

        attendance_mapping_data['IsParticipant'] = attendance_mapping_data.apply(self.is_participant, axis=1)
        attendance_mapping_data['ConcatId'] = attendance_mapping_data.apply(self.get_concat_id, axis=1)
        self.attendance_mapping = pd.Series(attendance_mapping_data['Group Id'].values,
                                            index=attendance_mapping_data.ConcatId).to_dict()

        keys_to_alter = []
        for key, value in self.attendance_mapping.items():
            if '&type=ANY' in key:
                keys_to_alter.append(key)

        for key in keys_to_alter:
            first_half_of_key = key.split('&type=')[0]
            self.attendance_mapping[first_half_of_key + '&type=P'] = self.attendance_mapping[key]
            self.attendance_mapping[first_half_of_key + '&type=NP'] = self.attendance_mapping[key]
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
        for failed_concat_id in failing_concat_ids:
            print(failed_concat_id)
        return attendance_frame

    @staticmethod
    def is_participant(row):
        type = row['Individual Type']
        if type == 'Participant':
            return 'P'
        elif type == '-- all others --':
            return 'NP'
        return 'ANY'

    @staticmethod
    def remove_single_quotes(value):
        return value.replace("'", "")

    @staticmethod
    def get_concat_id(row):
        result = (row['Ministry'] + '&activity=' + row['Activity'] + '&roster=' + replace_any(row['Roster']) + '&type=' + row['IsParticipant'])
        job = row['Job']
        if job in jobs_that_require_a_special_map:
            result = result + '&job=' + job
        return result.replace("'", "").replace(' ', '')

    def fail(self, row):
        failing_concat_ids.add(row['ConcatId'])
        return '0'

    def get_group_id(self, row):
        # Try for exact match on concat id
        try:
            return self.attendance_mapping[row['ConcatId']]
        except:
            # Try for match ignoring job
            concat_id_split_on_job = row['ConcatId'].split('&job=')
            concat_id_without_job = concat_id_split_on_job[0]
            try:
                return self.attendance_mapping[concat_id_without_job]
            except:
                # Try for match on just ministry activity and job if job exists
                if len(concat_id_split_on_job) > 1:
                    concat_id_ministry_activity_and_job = row['ConcatId'].split('&roster=')[0] + '&roster=&job=' + row['ConcatId'].split('&job=')[1]
                    try:
                        return self.attendance_mapping[concat_id_ministry_activity_and_job]
                    except:
                        return self.fail(row)
                else:
                    return self.fail(row)

