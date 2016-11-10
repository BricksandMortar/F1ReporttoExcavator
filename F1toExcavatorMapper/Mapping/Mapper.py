import os
import pandas as pd

from F1toExcavatorMapper.Mapping import BuilderFactory
from F1toExcavatorMapper.Mapping.Mode import Mode

from F1toExcavatorMapper.Exception.MappingFileNotFound import MappingFileNotFound
from F1toExcavatorMapper.Mapping import SourceCSVType
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
    return os.path.join(split_path[0], target_file_type.name.lower() + '.csv')


def run(source_file_path, target_file_type: TargetCSVType, source_type: SourceCSVType):
    mode = source_type.mode
    set_up(source_file_path, target_file_type, mode)
    data = CSVOperations.read_file_without_check(source_file_path)
    builder = BuilderFactory.get_builder(target_file_type)
    output_data = builder.map(data, source_type)

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
