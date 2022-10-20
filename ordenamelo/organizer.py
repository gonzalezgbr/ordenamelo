"""This is ordenamelo's main module."""

import os
from pathlib import Path
import sys

import pdfplumber


from ordenamelo.configurator import Configurator


class Organizer:
    """Provides search, rename and move receipts functionality."""

    def __init__(self):
        self.__config = Configurator()

    def organize(self, rename_only=False):
        """Public interface, coordinates searching the files, renaming and, optionally, 
        moving them."""
        print(">>> INICIANDO ORDEN...")
        # Search files that have a keyword in the filename, get list of fullpaths.
        fullpaths = self.__search_all()
        if not fullpaths:
            print('>>> Nada que hacer!')
            print(">>> CHAO (╯°□°)╯")
            sys.exit(0)

        # Rename found files.
        print('>>> Renombrando comprobantes...')
        renamed_full_filenames = []
        for fullpath in fullpaths:
            # get filename+extension or None
            new_full_filename = self.__rename(fullpath)
            if new_full_filename is not None:
                renamed_full_filenames.append(new_full_filename)
        print(f'>>> {len(renamed_full_filenames)} archivos renombrados.')
        if not renamed_full_filenames:
            print(">>> CHAO (╯°□°)╯")
            sys.exit(0)

        # Move files, unless it was explicitely chosen by user not to.
        if not rename_only:
            print('>>> Moviendo archivos...')
            count = 0
            for full_filename in renamed_full_filenames:
                # True if move was successfull
                if self.__move(full_filename):
                    count += 1
            print(f'>>> {count} archivos movidos.')

        print(">>> TODO EN ORDEN, OJALÁ TE DURE! (╯°□°)╯")

    def __search_all(self):
        """Search the payment receipts in the origin dir using the keywords in config
         file."""
        print('>>> Buscando comprobantes...')
        pdf_fullpaths = [entry for entry in self.__config.get_config_origin_path().iterdir()
                         if entry.is_file() and entry.suffix == '.pdf']
        selected_fullpaths = []
        for keyword in self.__config.get_config_keywords():
            selected_fullpaths.extend([fullpath for fullpath in pdf_fullpaths 
                                                    if keyword in fullpath.name.lower()])
        if selected_fullpaths:
            print(f'>>> {len(selected_fullpaths)} comprobantes encontrados:')
            print('>>> '+'\n>>> '.join([fullpath.name for fullpath in selected_fullpaths]))
        else:
            print('>>> No se encontraron comprobantes.')

        return selected_fullpaths

    def __make_new_filename_payment(self, pdf_metadata, v):
        """Make new payment receipt filename using year, month and the rule value from 
        the config file"""

        creation_date = pdf_metadata['CreationDate'][2:8].strip()
        formatted_date = creation_date[:4] + '-' + creation_date[4:6]
        new_filename = formatted_date + '-' + v

        return new_filename

    def __make_new_filename_transfer(self, pdf_text, pdf_metadata):
        """Make new transfer filename using, recipient's name, amount and full date.
         Works with transfer receipts from Santander and Nación Argentina banks."""

        creation_date = pdf_metadata['CreationDate'][2:10].strip()
        if 'canal' in pdf_text:
            money = pdf_text[pdf_text.find('importe: $ ') + 11:pdf_text.find(',')].replace('.', '').strip()
            name = pdf_text[pdf_text.find('destinatario: ') + 14:pdf_text.find('referencia')-30].title().replace(' ', '').strip()
        else:
            money = pdf_text[pdf_text.find('$ ') + 2:pdf_text.find(',')].replace('.', '').strip()
            name = pdf_text[pdf_text.find('transferencia') + 13:pdf_text.find('$')].title().replace(' ', '').strip()
        formatted_date = creation_date[:4] + '-' + creation_date[4:6] + '-' + creation_date[6:]
        if len(name) > 20:
            name = name[:20]
        new_filename = formatted_date + '-' + name + '-' + money

        return new_filename

    def __rename_file(self, fullpath, filename, extension):
        """Rename file with newname, but if it already exists do nothing."""
        full_filename = filename + extension
        try:
            Path.rename(fullpath, fullpath.parent / full_filename)
            print(f'>>> {fullpath.name} renombrado a {full_filename}')
            return full_filename
        except FileExistsError:
            print(f'>>> {full_filename} NO renombrado, ya existe en {fullpath.parent}')

            return None

    def __rename(self, fullpath):
        """Rename payment and transfer receipts."""
        with pdfplumber.open(fullpath) as pdf:
            pdf_text = pdf.pages[0].extract_text().strip().lower()
            pdf_metadata = pdf.metadata
        extension = '.pdf'
        for k, v in self.__config.get_config_rules().items():
            if k.lower() in pdf_text:
                new_filename = self.__make_new_filename_payment(pdf_metadata, v)
                return self.__rename_file(fullpath, new_filename, extension)

        if 'transferencia' in fullpath.name.lower():
            new_filename = self.__make_new_filename_transfer(pdf_text, pdf_metadata)
            return self.__rename_file(fullpath, new_filename, extension)

        # If I got here, it means there's no rule to apply and its not a transfer.
        print(f'>>> No se encuentra regla para {fullpath.name}.')

    def __is_transfer(self, full_filename):
        """Check if file is a transfer recepit."""
        return True if full_filename[8:10].isnumeric() else False

    def __move(self, full_filename):
        """Move file to new destination."""
        # year = datetime.now().year
        # parsed_pdf = parser.from_file(str(self._origin.joinpath(file)))
        fullpath_origin = self.__config.get_config_origin_path() / full_filename
        with pdfplumber.open(fullpath_origin) as pdf:
            pdf_creation_date = pdf.metadata['CreationDate']
        year = pdf_creation_date[2:6]

        if self.__is_transfer(full_filename):
            path_destination = self.__config.get_config_destination_path() / str(year) / 'transferencias'
        else:
            path_destination = self.__config.get_config_destination_path() / str(year)

        if not path_destination.exists():
            path_destination.mkdir(parents=True, exist_ok=False)
        if not path_destination.joinpath(full_filename).exists():
            fullpath_origin.replace(path_destination / full_filename)
            print(f'>>> {full_filename} movido a {path_destination}.')
            return True
        else:
            print(f'>>> {full_filename} NO movido, ya existe en {path_destination}.')

    def configure(self):
        """Open the config file in the OS default text editor."""

        os.system('notepad ' + str(self.__config.get_config_filepath()))
