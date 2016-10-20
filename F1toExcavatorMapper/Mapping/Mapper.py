import os
import pandas as pd

from F1toExcavatorMapper.Exception.MappingFileNotFound import MappingFileNotFound
from F1toExcavatorMapper.Mapping.Family.FamilyBuilder import build_family_frame
from F1toExcavatorMapper.Mapping.Individual.IndividualBuilder import build_individual_frame
from F1toExcavatorMapper.Utils import CSVOperations
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType


def get_target_file_path(mode:TargetCSVType, source_file_path):
    split_path = os.path.split(source_file_path)
    if mode == TargetCSVType.INDIVIDUAL:
        return os.path.join(split_path[0], 'Individual.csv')
    elif mode == TargetCSVType.FAMILY:
        return os.path.join(split_path[0], 'Family.csv')


def run(source_file_path, mode):
    source_file_path = r"C:\Users\arran\Dropbox\Bricks and Mortar\RVC_Data_Mapping\X9400_no_attributes.csv"
    existing_ids = set_up(source_file_path, mode)
    data = CSVOperations.read_file_without_check(source_file_path)

    output_data = build_output_frame(data, mode)
    CSVOperations.write_file(get_target_file_path(mode, source_file_path), output_data)


def set_up(source_file_path, mode):
    source_file_path = source_file_path
    mode = mode
    target_file_path = get_target_file_path(mode, source_file_path)

    if not CSVOperations.check_file_exists(source_file_path):
        raise MappingFileNotFound

    existing_ids = None
    if not CSVOperations.check_file_exists(target_file_path):
        CSVOperations.create_file(target_file_path, mode)
    else:
        existing_ids = get_existing_ids(target_file_path, mode)
    return existing_ids


def get_existing_ids(file_path, mode):
    target_data_frame = CSVOperations.read_file(file_path, mode)
    if target_data_frame is not None:
        existing_ids = target_data_frame[mode.primary_key].tolist()
        return existing_ids
    else:
        return None


def build_output_frame(data, mode):
    if mode == TargetCSVType.INDIVIDUAL:
        return build_individual_frame(data)
    elif mode == TargetCSVType.FAMILY:
        return build_family_frame(data)

run(None, TargetCSVType.INDIVIDUAL)