import argparse

import yaml

import F1toExcavatorMapper.Mapping.Mapper as Mapper
from F1toExcavatorMapper.Exception import SettingsFileNotFound
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType


def run():
    settings = get_settings()
    for file_type, source_file_path in settings.items():
        source_type = get_source_csv_type(file_type)
        for target_type in source_type.target_types:
            Mapper.run(source_file_path, target_type, source_type)


def get_settings():
    parser = argparse.ArgumentParser(
        description="Maps F1 report exports into a format for importing into Rock with Excavator")
    parser.add_argument('--s', "--settings", required=True, help="The file where the settings are stored",
                        dest='settings_location')
    args = parser.parse_args()
    settings_location = args.__dict__['settings_location']
    with open(settings_location, 'r') as file:
        try:
            settings = yaml.load(file)
            return settings
        except:
            raise SettingsFileNotFound

def get_source_csv_type(file_type):
    for source_type in SourceCSVType:
        if source_type.name.lower() == file_type:
            return source_type
    return None


run()
