from F1toExcavatorMapper import CSVOperations
from F1toExcavatorMapper.Exception.MappingFileNotFound import MappingFileNotFound
from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType


def get_target_file(mode):
    pass


def set_up(source_file_path, mode, source_type):
    source_file_path = source_file_path
    mode = mode
    target_file_name = get_target_file(mode)

    if not CSVOperations.check_file_exists(source_file_path):
        raise MappingFileNotFound

    existing_ids = None
    if not CSVOperations.check_file_exists(target_file_name):
        CSVOperations.create_file(target_file_name, mode)
    else:
        existing_ids = get_existing_ids(target_file_name, mode)
        #Get existing ids


def get_existing_ids(file_path,  mode):
    target_data_frame = CSVOperations.read(file_path, None, None)
    return target_data_frame[mode.primary_key].tolist()
