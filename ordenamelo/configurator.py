"""This module manages the configuration data for ordenamelo."""

import configparser
from pathlib import Path
import sys


class Configurator:
    """Process the cfg file to get paths, keywords and rules."""

    def __init__(self):
        """Set the path of the cfg. config file and load config contents to self."""

        self.__filepath = Path(__file__).parent.resolve().joinpath('data/config.cfg')
        self.__config = configparser.ConfigParser()
        self.__config.read(self.__filepath)
        try:
            self.__paths = self.__config['paths']
            self.__keywords = self.__config['keywords']
            self.__rules = self.__config['rules']
        except KeyError:
            print(">>> ERROR! No se encuentra el archivo de configuración o tiene errores.")
            sys.exit(1)

    def get_config_origin_path(self):
        """Return search path for the receipts."""

        return Path(self.__paths['origin'])

    def get_config_destination_path(self):
        """Return destination path for the renamed receipts."""

        return Path(self.__paths['dest'])

    def get_config_keywords(self):
        """Return the keywords to identify the files to rename."""

        return self.__keywords

    def get_config_rules(self):
        """Return the rules that indicate given a value in the file's content (key),
        what is the word to rename it with (value)."""

        return self.__rules

    def get_config_filepath(self):
        """Return the .cfg config filepath."""

        return self.__filepath
