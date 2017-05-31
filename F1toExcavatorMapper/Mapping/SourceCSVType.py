from enum import Enum

from F1toExcavatorMapper.Mapping.Mode import Mode
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType


class SourceCSVType(Enum):
    INDIVIDUAL_HOUSEHOLD = (('Individual_ID', 'Member_Envelope', 'Barcode', 'Title', 'Prefix', 'First_Name', 'Goes_By',
                             'Middle_Name', 'Last_Name', 'Former_Name', 'Suffix', 'Household_Position', 'Gender', 
                             'Marital_Status', 'Age', 'DOB', 'Status_Group', 'Status', 'Substatus', 'status_date', 
                             'Status_Comment', 'Tag_Comment', 'Opt_In_Directory', 'Unsubscribed', 'Former_Denomination',
                             'School_Type', 'School', 'Employer', 'Occupation', 'Occupation_Desc', 'First_Record',
                             'Last_Updated', 'Last_Attended', 'Last_Activity_Attended', 'Last_Roster_Attended',
                             'last_contact_date', 'Last_Gave_On', 'Last_Gift', 'Preferred_Phone', 'Mobile_Phone', 
                             'Work_Phone', 'Emergency_Phone', 'Preferred_Email', 'InFellowship_Email',  'Personal_Email',
                             'Facebook', 'Linkedin', 'Twitter', 'Household_Id', 'Household_Name', 'HH_First_Name',
                             'HH_Last_Name', 'HH_Preferred_Phone', 'HH_Preferred_Email', 'HH_Head_Name', 'HH_Head_DOB',
                             'HH_Head_Status', 'HH_Head_SubStatus', 'HH_Head_First_Record', 'HH_Head_Phone',
                             'HH_Head_Email', 'HH_Spouse_Name', 'HH_Spouse_DOB', 'HH_Spouse_Status',
                             'HH_Spouse_SubStatus', 'HH_Spouse_First_Record', 'HH_Spouse_Phone', 'HH_Spouse_Email',
                             'HH_Children', 'HH_Children_Ages', 'HH_Childs_Last_Attendance', 'AddressID', 
                             'Street_Address', 'City', 'State_Province', 'Postal_Area', 'Postal_Code_5',
                             'Postal_Code', 'County', 'Country', 'Address_Comments', 'Verified', 'Attribute_Group',
                             'Attribute', 'Created_Date', 'Start_Date', 'End_Date', 'Pastor_Staff', 'Department',
                             'Comment'), (TargetCSVType.FAMILY, TargetCSVType.INDIVIDUAL), Mode.CREATE)

    ATTRIBUTES = (('individual_id_1', 'attribute_group_name', 'attribute_name', 'start_date', 'end_date', 'comment'),
                  [TargetCSVType.INDIVIDUAL], Mode.APPEND)

    GIVING = (('Gift_ID', 'Transaction_ID', 'Contributor_Type', 'Giving_Unit_ID', 'Giving_Unit_Name', 
               'Giving_Unit_Contact_Name1', 'Contributor_ID', 'Contributor_Name', 'Member_Envelope', 'DOB', 'Age', 
               'Textbox59', 'Marital_Status', 'Status_Group', 'Status', 'SubStatus', 'status_date', 'Preferred_Phone',
               'Preferred_Email', 'Street_1', 'Street_2', 'Street_3', 'City', 'State_Province', 'Postal_Area',
               'Postal_Code_Short', 'Postal_Code', 'County', 'Country', 'Last_Attended', 'First_Gift_Date',
               'First_Gift_Amount', 'Second_Gift_Date', 'Second_Gift_Amount', 'Third_Gift_Date', 'Third_Gift_Amount',
               'Last_Gift_Date', 'Last_Gift_Amount', 'Largest_Gift_Date', 'Largest_Gift_Amount', 'Activity',
               'Activity_Time', 'Batch_Date', 'Batch_Name', 'Batch_Status', 'Batch_Entered', 'Fund_Code', 'Fund',
               'Fund_Type', 'SubFund_Code', 'SubFund', 'Pledge_Drive1', 'Contributor_Pledge_Amount',
               'Giving_Unit_Amount_Pledged', 'GL_Post_Date', 'General_Ledger', 'Entered_by_User', 'Originating_Source',
               'Frequency', 'Created_Date', 'Created_Time', 'Received_Date', 'Received_Time', 'Last_Updated_Date',
               'Gift_Aid_Date', 'Gift_Aid_ID', 'Type', 'SubType', 'Bank_Card_Type', 'Bank_Card_Last_4', 'Reference',
               'Contribution_Attributes', 'Amount', 'True_Value', 'Liquidation_Costs',
               'Memo'), [TargetCSVType.CONTRIBUTION, TargetCSVType.BATCH], Mode.CREATE)

    ATTRIBUTE_NOTES = (('individual_id_1', 'attribute_group_name', 'attribute_name', 'start_date', 'end_date', 
                        'comment'), [TargetCSVType.NOTE], Mode.CREATE)

    REQUIREMENTS = (('Individual Id', 'Name', 'Status', 'Date', 'Portal User'), [TargetCSVType.INDIVIDUAL], Mode.APPEND)

    ATTENDANCE = (('Household ID', 'Household Name', 'Individual ID', 'Last Name', 'First Name', 'Status Group',
                   'Status', 'Sub Status', 'Status Date', 'DOB', 'Age', 'Gender', 'Marital Status', 'Preferred Email',
                   'School', 'First Record Date', 'Last Updated', 'Address 1', 'City', 'State Province', 'Postal Code',
                   'County', 'Country', 'Home Phone', 'Ministry', 'Activity', 'Roster', 'Break Out Group', 'Date',
                   'Time', 'Individual Type', 'Job', 'Group Name', 'Group Type Name', 'Campus Name'),
                  [TargetCSVType.ATTENDANCE], Mode.CREATE)

    SMALL_GROUP = (('Household ID', 'Household Name', 'Individual ID', 'Last Name', 'First Name', 'Status Group',
                   'Status', 'Sub Status', 'Status Date', 'DOB', 'Age', 'Gender', 'Marital Status', 'Preferred Email',
                   'School', 'First Record Date', 'Last Updated', 'Address 1', 'City', 'State Province', 'Postal Code',
                   'County', 'Country', 'Home Phone', 'Ministry', 'Activity', 'Roster', 'Break Out Group', 'Date',
                   'Time', 'Individual Type', 'Job', 'Group Name', 'Group Type Name', 'Campus Name'),
                  [TargetCSVType.ATTENDANCE], Mode.APPEND)

    ATTENDANCE_MAPPING = (('F1 Ministry', 'F1 Activity', 'F1 Roster', 'Individual Type', 'Group Type Id', 'Group Id',
                           'Group Name'), [TargetCSVType.ATTENDANCE], Mode.APPEND)

    def __init__(self, columns, target_types, mode):
        self.columns = columns
        self.target_types = target_types
        self.mode = mode
