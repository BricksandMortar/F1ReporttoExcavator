import csv
import os
from pathlib import Path
import pandas as pd

from F1toExcavatorMapper.Exception.IncorrectHeaders import IncorrectHeaders

def get_header_count(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return len(reader.fieldnames)


def check_headers_match(file_name, file_type):
    correct_headers = __get_headers(file_type)
    with open(file_name, 'r', newline='') as file:
        reader = pd.read_csv(file)
        return tuple(reader.columns.values) == correct_headers


def check_data_frame_headers_match(data_frame:pd.DataFrame, file_type):
    correct_headers = __get_headers(file_type)
    return tuple(data_frame.columns.values) == correct_headers


def check_file_exists(file_path):
    file = Path(file_path)
    return file.is_file()


def create_file(file_name, file_type):
    __touch(file_name)
    __write_headers_to_csv(file_name, __get_headers(file_type))


def write_file(file_path, data_frame):
    with open(file_path, 'a', newline='') as file:
        data_frame.to_csv(file, header=False, index=False )


def read_file(file_path, file_type):
    data = __read_file(file_path)
    headers_match = check_data_frame_headers_match(data, file_type)
    if not headers_match:
        raise IncorrectHeaders(file_path + 'headers do not match', "")


def read_file_without_check(file_path):
    return __read_file(file_path)


def __read_file(file_path):
    with open(file_path, 'r') as file:
        data = pd.read_csv(file)
    return data


def __get_headers(file_type):
    return file_type.columns


def __touch(file_name, mode=0o666, dir_fd=None, **kwargs):
    # http://stackoverflow.com/questions/1158076/implement-touch-using-python
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(file_name, flags=flags, mode=mode, dir_fd=dir_fd)) as file:
        os.utime(file.fileno() if os.utime in os.supports_fd else file_name,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)


def __write_headers_to_csv(filename, fields):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fields, quoting=csv.QUOTE_MINIMAL, quotechar='"')
        writer.writeheader()



