import os
import pandas as pd
from F1toExcavatorMapper.Mapping.Mode import Mode

from F1toExcavatorMapper.Exception.MappingFileNotFound import MappingFileNotFound
from F1toExcavatorMapper.Mapping import SourceCSVType
from F1toExcavatorMapper.Mapping.Family.FamilyBuilder import build_family_frame
from F1toExcavatorMapper.Mapping.Individual import IndividualBuilder
from F1toExcavatorMapper.Utils import CSVOperations
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType


def get_target_file_path(target_file_type: TargetCSVType, source_file_path):
    split_path = os.path.split(source_file_path)
    if target_file_type == TargetCSVType.INDIVIDUAL:
        return os.path.join(split_path[0], 'Individual.csv')
    elif target_file_type == TargetCSVType.FAMILY:
        return os.path.join(split_path[0], 'Family.csv')


def get_index_of_header(target_type: TargetCSVType):
    headers = SourceCSVType.SourceCSVType.INDIVIDUAL_HOUSEHOLD.columns
    primary_key = __get_source_file_primary_key(target_type)
    for index in range(len(headers)):
        if headers[index] == primary_key:
            return index
    return None


def __get_source_file_primary_key(target_type: TargetCSVType):
    if target_type == TargetCSVType.INDIVIDUAL:
        return 'Individual_ID'
    elif target_type == TargetCSVType.FAMILY:
        return 'Household_Id'


def run(source_file_path, target_file_type: TargetCSVType, source_type):
    mode = source_type.mode
    set_up(source_file_path, target_file_type, mode)
    data = CSVOperations.read_file_without_check(source_file_path, get_index_of_header(mode))

    output_data = build_output_frame(data, target_file_type, source_type, source_file_path)

    target_file_path = get_target_file_path(target_file_type, source_file_path)
    if mode == Mode.APPEND:
        CSVOperations.delete_write(target_file_path, output_data)
    else:
        CSVOperations.write_file(get_target_file_path(mode, source_file_path), output_data)


def set_up(source_file_path, target_file_type, mode):
    target_file_path = get_target_file_path(target_file_type, source_file_path)

    if not CSVOperations.check_file_exists(source_file_path):
        raise MappingFileNotFound

    if CSVOperations.check_file_exists(target_file_path) and mode != Mode.APPEND:
        CSVOperations.delete_file(target_file_path)

    if not CSVOperations.check_file_exists(target_file_path):
        CSVOperations.create_file(target_file_path, target_file_type)

    # existing_ids = None
    # if not CSVOperations.check_file_exists(target_file_path):
    #     CSVOperations.create_file(target_file_path, mode)
    # else:
    #     existing_ids = get_existing_ids(target_file_path, mode)
    # return existing_ids


# FIXME #1 Resumption with existing ids is not supported
# def get_existing_ids(file_path, mode):
#     target_data_frame = CSVOperations.read_file(file_path, mode, get_index_of_header(mode))
#     if target_data_frame is not None:
#         existing_ids = target_data_frame[mode.primary_key].tolist()
#         return existing_ids
#     else:
#         return None


def build_output_frame(data, target_type, source_type, source_file_path):
    if target_type == TargetCSVType.INDIVIDUAL:
        if source_type == SourceCSVType.SourceCSVType.INDIVIDUAL_HOUSEHOLD:
            return IndividualBuilder.build_individual_core_frame(data)
        elif source_type == SourceCSVType.SourceCSVType.ATTRIBUTES:
            return IndividualBuilder.add_attributes_to_frame(data, get_target_file_path(target_type, source_file_path))
    elif target_type == TargetCSVType.FAMILY:
        return build_family_frame(data)

run()