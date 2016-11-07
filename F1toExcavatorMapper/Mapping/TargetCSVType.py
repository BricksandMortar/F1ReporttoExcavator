from enum import Enum

from F1toExcavatorMapper.Mapping.Family.FamilyBuilder import FamilyBuilder
from F1toExcavatorMapper.Mapping.Finances import FinancialBuilder
from F1toExcavatorMapper.Mapping.Individual.IndividualBuilder import IndividualBuilder


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
                               ), IndividualBuilder.Instance)

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
                           'SecondaryCountry'), FamilyBuilder.Instance)

    BATCH = ('BatchId', ('BatchId', 'BatchName', 'BatchName', 'BatchDate', 'Batch'),
             FinancialBuilder.FinancialBuilder.Instance())

    def get_builder(self):
        return self.builder()

    def __init__(self, primary_key, columns, builder):
        self.primary_key = primary_key
        self.columns = columns
        self.builder = builder
