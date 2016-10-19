from pandas import Series
import pandas as pd

from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType


def build_family_frame(data):
    family_frame = data.loc[:, ['Household_Id', 'Household_Name', 'Street_Address', 'City', 'State_Province',
                                'Postal_Code_5']]
    family_frame = family_frame.rename(columns={'Household_Id': 'FamilyId', 'Household_Name': 'FamilyName',
                                                'Street_Address': 'Address', 'State_Province': 'State',
                                                'Postal_Code_5': 'ZipCode'})

    family_frame = pd.concat([family_frame, pd.DataFrame(columns=('Country', 'CreatedDate', 'Campus', 'Address2', 'SecondaryAddress',
                                                   'SecondaryAddress2',
                                                   'SecondaryCity',
                                                   'SecondaryState',
                                                   'SecondaryZip',
                                                   'SecondaryCountry'))])
    family_frame.fillna({'Country': 'US'})
    family_frame.fillna({'Campus': 'MAIN'})
    #Fixme I make all your data go away
    # family_frame = family_frame['State'].apply(clean_up_state)
    family_frame = family_frame[list(TargetCSVType.FAMILY.columns)]
    return family_frame


def clean_up_state(value):
    if type(value) is str and not value.isnumeric():
        value = value[:2]
        value.upper()
    else:
        return ""

