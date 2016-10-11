import csv
from pathlib import Path

individual_headers = ['FamilyId',
                      'FamilyName',
                      'CreatedDate',
                      'PersonId',
                      'Prefix',
                      'FirstName',
                      'NickName',
                      'MiddleName',
                      'LastName',
                      'Suffix',
                      'FamilyRole',
                      'MaritalStatus',
                      'ConnectionStatus',
                      'RecordStatus',
                      'IsDeceased',
                      'HomePhone',
                      'MobilePhone',
                      'WorkPhone',
                      'SMS Allowed?',
                      'Email',
                      'IsEmailActive',
                      'Allow Bulk Email?',
                      'Gender',
                      'DateOfBirth',
                      'School',
                      'GraduationDate',
                      'AnniversaryDate',
                      'GeneralNote',
                      'MedicalNote',
                      'SecurityNote',
                      ]


def check_headers_exist(filename):
    with open(filename, 'rb') as file:
        return csv.Sniffer().has_header(file.read(1024))


def check_headers_match(filename):
        with open(filename, 'rb') as file:
            reader = csv.reader(file)
            reader.next()
            return reader.fieldnames == individual_headers


def check_file_exists(file_path):
    file = Path(file_path)
    return file.is_file()


def write_to_csv(filename, fields):
    with open(filename) as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, quotechar='"')
        for row in writer:
            print(row)
