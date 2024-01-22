"""This module manages the configuration data for ordenamelo."""

import configparser
from pathlib import Path
import sys

from pathvalidate import sanitize_filepath


class Configurator:
    """Process the cfg file to get paths, keywords and rules."""

    def __init__(self):
        """Set the path of the cfg. config file and load config contents to self."""

        self.filepath = Path(__file__).parent.resolve().joinpath('data/config.cfg')
        self._config = configparser.ConfigParser()
        self._config.read(self.filepath)
        try:
            self.origin_path, self.destination_path = self._validate_user_paths(self._config['paths'])
            self.destination_path = Path(self._config['paths']['dest'])
            self.keywords = self._config['keywords']
            self.rules = self._config['rules']
        except KeyError:
            print(">>> ERROR! No se encuentra el archivo de configuración o tiene errores.")
            sys.exit(1)

    def _validate_user_paths(self, user_paths):
        """Make sure the user entered paths are valid and exist."""
        origin_path = Path(sanitize_filepath(user_paths['origin']))
        destination_path = Path(sanitize_filepath(user_paths['dest']))
        
        return origin_path, destination_path

    # def get_config_destination_path(self):
    #     """Return destination path for the renamed receipts."""

    #     return Path(self._paths['dest'])

    # def get_config_keywords(self):
    #     """Return the keywords to identify the files to rename."""

    #     return self._keywords

    # def get_config_rules(self):
    #     """Return the rules that indicate given a value in the file's content (key),
    #     what is the word to rename it with (value)."""

    #     return self._rules

    # def get_config_filepath(self):
    #     """Return the .cfg config filepath."""

    #     return self._filepath
