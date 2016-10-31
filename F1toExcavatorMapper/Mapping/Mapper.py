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
    """
    Returns the file path for a new target file.
    :param target_file_type: The type of file to be created
    :param source_file_path: The file path of the file that contains the target file's source information
    :return: The path where the new target file should be created
    """
    split_path = os.path.split(source_file_path)
    return os.path.join(split_path[0], target_file_type.name.lower())

def get_index_of_header(target_type: TargetCSVType, source_type: SourceCSVType):
    headers = source_type.columns
    # Potential keys that could be primary keys for the source CSV
    candidate_primary_keys = __get_source_file_primary_keys(target_type)
    for index in range(len(headers)):
        if headers[index] in candidate_primary_keys:
            return index
    return None


def __get_source_file_primary_keys(target_type: TargetCSVType):
    """
    Given a target CSV type, it returns a source file's key to identify the target's information
    :param target_type: The target CSV type
    :return: The key for the Target CSV's source to identify the target CSVs information
    """
    return target_type.source_primary_key


def run(source_file_path, target_file_type: TargetCSVType, source_type: SourceCSVType):
    mode = source_type.mode
    set_up(source_file_path, target_file_type, mode)
    data = CSVOperations.read_file_without_check(source_file_path, get_index_of_header(target_file_type, source_type))

    output_data = build_output_frame(data, target_file_type, source_type, source_file_path)

    target_file_path = get_target_file_path(target_file_type, source_file_path)
    if mode == Mode.APPEND:
        CSVOperations.delete_write(target_file_path, output_data)
    else:
        CSVOperations.write_file(get_target_file_path(target_file_type, source_file_path), output_data)


def set_up(source_file_path, target_file_type, mode):
    target_file_path = get_target_file_path(target_file_type, source_file_path)

    if not CSVOperations.check_file_exists(source_file_path):
        raise MappingFileNotFound('Mapping File Not Found', source_file_path)

    if CSVOperations.check_file_exists(target_file_path) and mode != Mode.APPEND:
        CSVOperations.delete_file(target_file_path)

    if not CSVOperations.check_file_exists(target_file_path):
        CSVOperations.create_file(target_file_path, target_file_type)


def build_output_frame(data, target_type, source_type, source_file_path):
    if target_type == TargetCSVType.INDIVIDUAL:
        if source_type == SourceCSVType.SourceCSVType.INDIVIDUAL_HOUSEHOLD:
            return IndividualBuilder.build_individual_core_frame(data)
        elif source_type == SourceCSVType.SourceCSVType.ATTRIBUTES:
            return IndividualBuilder.add_attributes_to_frame(data, get_target_file_path(target_type, source_file_path))
    elif target_type == TargetCSVType.FAMILY:
        return build_family_frame(data)