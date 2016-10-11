import csv
import os
from f1toexcavatormap import Final
from pathlib import Path

def get_header_count(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return len(reader.fieldnames)

def check_headers_match(filename):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            return tuple(reader.fieldnames) == Final.individual_headers


def check_file_exists(file_path):
    file = Path(file_path)
    return file.is_file()


def create_file(file_name, header_fields):
    __touch(file_name)
    __write_headers_to_csv(file_name, header_fields)

# http://stackoverflow.com/questions/1158076/implement-touch-using-python
def __touch(file_name, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(file_name, flags=flags, mode=mode, dir_fd=dir_fd)) as file:
        os.utime(file.fileno() if os.utime in os.supports_fd else file_name,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)


def __write_headers_to_csv(filename, fields):
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fields, quoting=csv.QUOTE_MINIMAL, quotechar='"')
        writer.writeheader()
