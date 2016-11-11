from F1toExcavatorMapper.Mapping.Family.FamilyBuilder import FamilyBuilder
from F1toExcavatorMapper.Mapping.Finances.FinancialBuilder import FinancialBuilder
from F1toExcavatorMapper.Mapping.Individual.IndividualBuilder import IndividualBuilder
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType


def get_builder(target_type: TargetCSVType):
    if target_type == TargetCSVType.INDIVIDUAL:
        return IndividualBuilder.Instance()
    elif target_type == TargetCSVType.FAMILY:
        return FamilyBuilder.Instance()
    elif target_type == TargetCSVType.CONTRIBUTION or target_type == TargetCSVType.BATCH:
        return FinancialBuilder.Instance()
