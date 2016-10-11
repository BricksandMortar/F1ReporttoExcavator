import csv
import os
from f1toexcavatormap import Final
from pathlib import Path


def check_headers_exist(filename):
    with open(filename, 'rb') as file:
        return csv.Sniffer().has_header(file.read(1024))


def check_headers_match(filename):
        with open(filename, 'rb') as file:
            reader = csv.reader(file)
            reader.next()
            return reader.fieldnames == Final.individual_headers


def check_file_exists(file_path):
    file = Path(file_path)
    return file.is_file()


def touch(file_name, mode=0o666, dir_fd=None, **kwargs):
    flags = os.O_CREAT | os.O_APPEND
    with os.fdopen(os.open(file_name, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
        os.utime(f.fileno() if os.utime in os.supports_fd else file_name,
                 dir_fd=None if os.supports_fd else dir_fd, **kwargs)


def write_to_csv(filename, fields):
    with open(filename) as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, quotechar='"')
        for row in writer:
            print(row)
