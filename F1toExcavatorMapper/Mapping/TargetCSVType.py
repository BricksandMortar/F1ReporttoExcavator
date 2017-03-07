from enum import Enum


class TargetCSVType(Enum):
    INDIVIDUAL = ("PersonId", ('FamilyId',
                               'FamilyName',
                               'CreatedDate',
                               'PersonId',
                               'Prefix',
                               'FirstName',
                               'NickName',
                               'MiddleName',
                               'LastName',
                               'Suffix',
                               'FamilyRole',
                               'MaritalStatus',
                               'ConnectionStatus',
                               'RecordStatus',
                               'IsDeceased',
                               'HomePhone',
                               'MobilePhone',
                               'WorkPhone',
                               'SMS Allowed?',
                               'Email',
                               'IsEmailActive',
                               'Allow Bulk Email?',
                               'Gender',
                               'DateOfBirth',
                               'School',
                               'GraduationDate',
                               'AnniversaryDate',
                               'GeneralNote',
                               'MedicalNote',
                               'SecurityNote',
                               ))

    FAMILY = ('FamilyId', ('FamilyId',
                           'FamilyName',
                           'CreatedDate',
                           'Campus',
                           'Address',
                           'Address2',
                           'City',
                           'State',
                           'ZipCode',
                           'Country',
                           'SecondaryAddress',
                           'SecondaryAddress2',
                           'SecondaryCity',
                           'SecondaryState',
                           'SecondaryZip',
                           'SecondaryCountry'))

    BATCH = ('BatchID', ('BatchID', 'BatchName', 'BatchDate', 'BatchAmount'))

    CONTRIBUTION = ('ContributionID', ('IndividualID',
                                       'FundName',
                                       'SubFundName',
                                       'FundGLAccount',
                                       'SubFundGLAccount',
                                       'FundIsActive',
                                       'SubFundIsActive',
                                       'ReceivedDate',
                                       'CheckNumber',
                                       'Memo',
                                       'ContributionTypeName',
                                       'Amount',
                                       'StatedValue',
                                       'ContributionID',
                                       'ContributionBatchID',
                                       'ContributorType'
                                       ))

    NOTE = ('note_id', ('individual_id_1',
                                 'attribute_group_name',
                                 'attribute_name',
                                 'start_date',
                                 'end_date',
                                 'comment',
                                 'note_id'
                        ))

    ATTENDANCE = ('Individual ID', ('Individual ID', 'Ministry', 'Activity', 'Roster', 'Job', 'Date', 'Time', 'Individual Type', 'GroupId'))

    def get_builder(self):
        return self.builder()

    def __init__(self, primary_key, columns):
        self.primary_key = primary_key
        self.columns = columns
