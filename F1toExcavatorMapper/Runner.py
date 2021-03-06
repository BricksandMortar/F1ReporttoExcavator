import argparse

import yaml

import F1toExcavatorMapper.Mapping.Mapper as Mapper
from F1toExcavatorMapper.Exception import SettingsFileNotFound
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType
from F1toExcavatorMapper.Utils import CSVOperations
from F1toExcavatorMapper.Utils.OrderedYamlLoader import ordered_load


def run():
    settings = get_settings()

    for file_type, source_file_path in settings.items():
        source_type = get_source_csv_type(file_type)
        for target_type in source_type.target_types:
            if isinstance(source_file_path, list):
                for path in source_file_path:
                    Mapper.run(path, target_type, source_type)
            else:
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
            settings = ordered_load(file, yaml.SafeLoader)
            return settings
        except:
            raise SettingsFileNotFound


def get_source_csv_type(file_type):
    for source_type in SourceCSVType:
        if source_type.name.lower() == file_type.lower():
            return source_type
    return None


run()
