import csv
import os
from pathlib import Path
import pandas as pd

from F1toExcavatorMapper.Mapping.TargetCSVType import TargetCSVType
from F1toExcavatorMapper.Constant import Excavator


def read(filename, number_to_read, offset):
    data_frame = pd.read_csv(filename, nrows=number_to_read, skiprows=offset)
    return data_frame


def get_header_count(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return len(reader.fieldnames)


def check_headers_match(filename, file_type):
    correct_headers = __get_headers(file_type)
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return tuple(reader.fieldnames) == correct_headers


def check_file_exists(file_path):
    file = Path(file_path)
    return file.is_file()


def create_file(file_name, file_type):
    __touch(file_name)
    __write_headers_to_csv(file_name, __get_headers(file_type))


def __get_headers(file_type):
    if file_type == TargetCSVType.individual:
        return Excavator.individual_csv_headers
    elif file_type == TargetCSVType.family:
        return Excavator.family_csv_headers


def __touch(file_name, mode=0o666, dir_fd=None, **kwargs):
    # http://stackoverflow.com/questions/1158076/implement-touch-using-python
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(file_name, flags=flags, mode=mode, dir_fd=dir_fd)) as file:
        os.utime(file.fileno() if os.utime in os.supports_fd else file_name,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)


def __write_headers_to_csv(filename, fields):
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fields, quoting=csv.QUOTE_MINIMAL, quotechar='"')
        writer.writeheader()



