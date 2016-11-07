from F1toExcavatorMapper.Utils.Singleton import Singleton


@Singleton
class FinancialBuilder:
    def __init__(self):
        self.batch_data = None

    def map(self, data, source_type):
        if self.batch_data is None:
            self.build_batches(data)
        else:
            self.build_contributions(data)

    def build_batches(self, data):
        # # By manually indexing we keep the column *and* get the index
        # self.individual_frame.index = self.individual_frame.set_index(['PersonId'])
        #
        # # Convert to DateTime
        # attribute_data['start_date'] = pd.to_datetime(attribute_data['start_date'])
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
        # # Select the subset of columns needed for mapping
        # individual_frame = data.loc[:,
        #                    ['Household_Id', 'Household_Name', 'First_Record', 'Individual_ID', 'First_Name', 'Goes_By',
        #                     'Middle_Name', 'Last_Name', 'Suffix', 'Marital_Status', 'Mobile_Phone', 'Work_Phone',
        #                     'Unsubscribed', 'Gender', 'DOB', 'Title', 'Prefix', 'Household_Position', 'Status',
        #                     'Status_Group', 'Preferred_Email', 'Personal_Email', 'InFellowship_Email']]
        # # Rename columns to match Excavator naming
        # individual_frame = individual_frame.rename(columns={'Household_Id': 'FamilyId', 'Household_Name': 'FamilyName',
        #                                                     'First_Record': 'CreatedDate', 'Individual_ID': 'PersonId',
        #                                                     'First_Name': 'FirstName', 'Last_Name': 'LastName',
        #                                                     'Marital_Status': 'MaritalStatus',
        #                                                     'Mobile_Phone': 'MobilePhone',
        #                                                     'Work_Phone': 'WorkPhone', 'DOB': 'DateOfBirth',
        #                                                     'Household_Position': 'FamilyRole',
        #                                                     'Status': 'ConnectionStatus',
        #                                                     'Status_Group': 'RecordStatus',
        #                                                     'InFellowship_Email': 'Email', 'Goes_By': 'NickName',
        #                                                     'Middle_Name': 'MiddleName'})
        # # Add blank columns that are required
        # individual_frame = pd.concat([individual_frame, pd.DataFrame(columns=('HomePhone', 'SMS Allowed?', 'School',
        #                                                                       'GraduationDate',
        #                                                                       'AnniversaryDate',
        #                                                                       'GeneralNote',
        #                                                                       'MedicalNote',
        #                                                                       'SecurityNote', 'IsDeceased',
        #                                                                       'IsEmailActive',
        #                                                                       'Allow Bulk Email?'))])
        # # Fill default values and apply mapping functions
        # individual_frame['SMS Allowed?'] = individual_frame['SMS Allowed?'].fillna('Yes')
        # individual_frame['Prefix'] = individual_frame.apply(self.get_prefix, axis=1)
        # individual_frame['FamilyRole'] = individual_frame['FamilyRole'].map(self.get_household_position)
        # individual_frame['IsDeceased'] = individual_frame.apply(self.get_is_deceased, axis=1)
        # individual_frame['RecordStatus'] = individual_frame['RecordStatus'].map(self.get_record_status)
        # individual_frame['Email'] = individual_frame.apply(self.get_email, axis=1)
        # individual_frame['IsEmailActive'] = individual_frame['Unsubscribed'].map(self.is_email_active)
        # individual_frame['Allow Bulk Email?'] = individual_frame['IsEmailActive']
        #
        # # Ensure that IDs are ints not floats
        # individual_frame['PersonId'] = individual_frame['PersonId'].astype(int)
        # individual_frame['FamilyId'] = individual_frame['FamilyId'].astype(int)
        #
        # # Reorder columns and select only the ones needed by Excavator
        # individual_frame = individual_frame[list(TargetCSVType.INDIVIDUAL.columns)]
        # self.individual_frame = individual_frame
        # return individual_frame
        pass