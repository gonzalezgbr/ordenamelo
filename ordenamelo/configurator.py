"""This module manages the configuration data for ordenamelo."""

import configparser
from pathlib import Path
import sys


class Configurator:
    """Process the cfg file to get paths, keywords and rules."""

    def __init__(self):
        """Set the path of the cfg. config file and load config contents to self."""

        self._filepath = Path(__file__).parent.resolve().joinpath('data/config.cfg')
        self._config = configparser.ConfigParser()
        self._config.read(self._filepath)
        try:
            self._paths = self._config['paths']
            self._keywords = self._config['keywords']
            self._rules = self._config['rules']
        except KeyError:
            print(">>> ERROR! No se encuentra el archivo de configuración o tiene errores.")
            sys.exit(1)

    def get_config_origin_path(self):
        """Return search path for the receipts."""

        return Path(self._paths['origin'])

    def get_config_destination_path(self):
        """Return destination path for the renamed receipts."""

        return Path(self._paths['dest'])

    def get_config_keywords(self):
        """Return the keywords to identify the files to rename."""

        return self._keywords

    def get_config_rules(self):
        """Return the rules that indicate given a value in the file's content (key),
        what is the word to rename it with (value)."""

        return self._rules

    def get_config_filepath(self):
        """Return the .cfg config filepath."""

        return self._filepath
