# configurator.py

"""Este módulo administra los datos de configuración de Ordenamelo."""

import configparser
from pathlib import Path
import sys


class Configurator:

    def __init__(self):
        """Setea la ruta del archivo de configuración .cfg, lee su contenido y carga los valores en self."""

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
        """Devuelve el Path donde se buscan los comprobantes."""

        return Path(self.__paths['origin'])

    def get_config_destination_path(self):
        """Devuelve el Path a donde se mueven los comprobantes, una vez renombrados."""

        return Path(self.__paths['dest'])

    def get_config_keywords(self):
        """Devuelve las palabras clave (Dict-like, solo claves)
        con las que se identifican los nombres de archivo a renombrar."""

        return self.__keywords

    def get_config_rules(self):
        """Devuelve las reglas (Dict-like) que indican,
        dado un valor en un archivo (clave), como debe renombrarse (valor)."""

        return self.__rules

    def get_config_filepath(self):
        """Devuelve la ruta (Path) donde se encuentra el archivo .cfg de configuración."""

        return self.__filepath