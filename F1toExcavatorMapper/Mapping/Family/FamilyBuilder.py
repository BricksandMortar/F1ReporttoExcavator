import re

from pandas import Series
import pandas as pd

from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType

regex = re.compile('[^a-zA-Z]')


def build_family_frame(data):
    # See columns in IndividualBuilder
    family_frame = data.loc[:, ['Household_Id', 'Household_Name', 'Street_Address', 'City', 'State_Province',
                                'Postal_Code_5']]
    family_frame = family_frame.rename(columns={'Household_Id': 'FamilyId', 'Household_Name': 'FamilyName',
                                                'Street_Address': 'Address', 'State_Province': 'State',
                                                'Postal_Code_5': 'ZipCode'})

    family_frame = pd.concat(
        [family_frame, pd.DataFrame(columns=('Country', 'CreatedDate', 'Campus', 'Address2', 'SecondaryAddress',
                                             'SecondaryAddress2',
                                             'SecondaryCity',
                                             'SecondaryState',
                                             'SecondaryZip',
                                             'SecondaryCountry'))])
    family_frame['Country'] = family_frame['Country'].fillna('US')
    family_frame['Campus'] = family_frame['Campus'].fillna('MAIN')
    family_frame['State'] = family_frame['State'].map(clean_up_state)
    family_frame['ZipCode'] = family_frame['ZipCode'].map(clean_up_zip)
    # Convert to Int
    family_frame['FamilyId'] = family_frame['FamilyId'].astype(int)
    family_frame = family_frame[list(TargetCSVType.FAMILY.columns)]
    family_frame = family_frame.drop_duplicates('FamilyId', keep='last')
    return family_frame


def clean_up_state(value):
    if type(value) is str and not value.isnumeric():
        value = regex.sub('', value)
        value = value.upper()
        if value.__len__() == 2:
            return value
        else:
            return ""
    else:
        return ""


def clean_up_zip(value):
    if str(value).__len__() == 5 and value != 99999:
        return value
    else:
        return ""
