import argparse

import yaml

import F1toExcavatorMapper.Mapping.Mapper as mapper
from F1toExcavatorMapper.Exception import SettingsFileNotFound
from F1toExcavatorMapper.Mapping.SourceCSVType import SourceCSVType


def run():
    settings = get_settings()
    for source_file_path, file_type in settings.items():
        source_type = get_source_csv_type(file_type)
        for target_type in source_type.target_types:
            mapper.run(source_file_path, target_type, source_type.mode)


def get_settings():
    parser = argparse.ArgumentParser(
        description="Maps F1 report exports into a format for importing into Rock with Excavator")
    parser.add_argument('--s', "--settings", required=True, help="The file where the settings are stored",
                        dest='settings_location')
    args = parser.parse_args()
    try:
        settings = yaml.load(args['settings_location'])
    except:
        raise SettingsFileNotFound
    return settings


def get_source_csv_type(settings_type):
    for source_type in SourceCSVType:
        if source_type.name.lower() == settings_type:
            return source_type
    return None

