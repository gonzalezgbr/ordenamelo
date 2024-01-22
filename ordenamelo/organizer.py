"""This is ordenamelo's main module."""

import os
from pathlib import Path
import platform
import sys

from pathvalidate import sanitize_filename
import pdfplumber

from ordenamelo.configurator import Configurator


class Organizer:
    """Provides search, rename and move receipts functionality."""

    def __init__(self):
        self._config = Configurator()

    def organize(self, rename_only=False):
        """Public interface, coordinates searching the files, renaming and, optionally,
         moving them."""
        print(">>> INICIANDO ORDEN...")
        self._check_user_filepaths()
        # Search files that have a keyword in the filename, get list of fullpaths.
        print(f'>>> Origen: {self._config.origin_path}')
        print(f'>>> Destino: {self._config.destination_path}')
        fullpaths = self._search_all()
        if not fullpaths:
            print('>>> Nada que hacer!')
            print(">>> CHAO (╯°□°)╯")
            sys.exit(0)

        # Rename found files.
        print('>>> Renombrando comprobantes...')
        renamed_full_filenames = []
        for fullpath in fullpaths:
            # get filename+extension or None
            new_full_filename = self._rename(fullpath)
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
                if self._move(full_filename):
                    count += 1
            print(f'>>> {count} archivos movidos.')

        print(">>> TODO EN ORDEN, OJALÁ TE DURE! (╯°□°)╯")

    def _check_user_filepaths(self):
        """Check if user filepaths exist"""
        ok = True
        if not self._config.origin_path.exists():
            print(f">>> ERROR! no existe el path de origen ({self._config.origin_path})")
            ok = False
        if not self._config.destination_path.exists():
            print(f">>> ERROR! no existe el path de destino ({self._config.destination_path})")
            ok = False
        if not ok:
            print(">>> Tienes que modificar el path que no existe o crear la carpeta correspondiente")
            sys.exit(1)

    def _search_all(self):
        """Search the payment receipts in the origin dir using the keywords in config
         file."""
        print('>>> Buscando comprobantes...')
        pdf_fullpaths = [entry for entry in self._config.origin_path.iterdir()
                         if entry.is_file() and entry.suffix == '.pdf']
        selected_fullpaths = []
        for keyword in self._config.keywords:
            selected_fullpaths.extend([fullpath for fullpath in pdf_fullpaths
                                                    if keyword in fullpath.name.lower()])
        if selected_fullpaths:
            print(f'>>> {len(selected_fullpaths)} comprobantes encontrados:')
            print('>>> '+'\n>>> '.join([fullpath.name for fullpath in selected_fullpaths]))
        else:
            print('>>> No se encontraron comprobantes.')

        return selected_fullpaths

    def _make_new_filename_payment(self, pdf_metadata, rule_value):
        """Make new payment receipt filename using year, month and the rule value from
         the config file"""

        creation_date = pdf_metadata['CreationDate'][2:8].strip()
        formatted_date = creation_date[:4] + '-' + creation_date[4:6]
        new_filename = formatted_date + '-' + sanitize_filename(rule_value)

        return new_filename

    def _make_new_filename_transfer(self, pdf_text, pdf_metadata):
        """Make new transfer filename using, recipient's name, amount and full date.
         Works with transfer receipts from Santander and Nación Argentina banks."""

        creation_date = pdf_metadata['CreationDate'][2:10].strip()
        if 'canal' in pdf_text:
            # Nacion Argentina Bank receipt
            money_start_idx = pdf_text.find('importe: $ ') + 11
            money_end_idx = pdf_text.find(',')
            name_start_idx = pdf_text.find('destinatario: ') + 14
            name_end_idx = pdf_text.find('referencia') - 30
        else:
            money_start_idx = pdf_text.find('$ ') + 2
            money_end_idx = pdf_text.find(',')
            name_start_idx = pdf_text.find('transferencia') + 13
            name_end_idx = pdf_text.find('$')

        money = pdf_text[money_start_idx : money_end_idx].replace('.', '').strip()
        name = sanitize_filename(pdf_text[name_start_idx : name_end_idx].title().replace(' ', '').strip())
        formatted_date = creation_date[:4] + '-' + creation_date[4:6] + '-' + creation_date[6:]
        if len(name) > 20:
            name = name[:20]
        new_filename = formatted_date + '-' + name + '-' + money

        return new_filename

    def _rename_file(self, fullpath, filename, extension):
        """Rename file with newname, but if it already exists do nothing."""
        full_filename = filename + extension
        try:
            Path.rename(fullpath, fullpath.parent / full_filename)
            print(f'>>> {fullpath.name} renombrado a {full_filename}')
            return full_filename
        except FileExistsError:
            print(f'>>> {full_filename} NO renombrado, ya existe en {fullpath.parent}')

            return None

    def _rename(self, fullpath):
        """Rename payment and transfer receipts."""
        with pdfplumber.open(fullpath) as pdf:
            pdf_text = pdf.pages[0].extract_text().strip().lower()
            pdf_metadata = pdf.metadata
        extension = '.pdf'
        for key, value in self._config.rules.items():
            if key.lower() in pdf_text:
                new_filename = self._make_new_filename_payment(pdf_metadata, value)
                return self._rename_file(fullpath, new_filename, extension)

        if 'transferencia' in fullpath.name.lower():
            new_filename = self._make_new_filename_transfer(pdf_text, pdf_metadata)
            return self._rename_file(fullpath, new_filename, extension)

        # If I got here, it means there's no rule to apply and its not a transfer.
        print(f'>>> No se encuentra regla para {fullpath.name}.')

    def _is_transfer(self, full_filename):
        """Check if file is a transfer recepit."""
        return full_filename[8:10].isnumeric()

    def _move(self, full_filename):
        """Move file to new destination."""
        # year = datetime.now().year
        # parsed_pdf = parser.from_file(str(self._origin.joinpath(file)))
        fullpath_origin = self._config.origin_path / full_filename
        with pdfplumber.open(fullpath_origin) as pdf:
            pdf_creation_date = pdf.metadata['CreationDate']
        year = pdf_creation_date[2:6]

        if self._is_transfer(full_filename):
            path_destination = self._config.destination_path / str(year) \
                                    / 'transferencias'
        else:
            path_destination = self._config.destination_path / str(year)

        if not path_destination.exists():
            path_destination.mkdir(parents=True, exist_ok=False)
        if not path_destination.joinpath(full_filename).exists():
            fullpath_origin.replace(path_destination / full_filename)
            print(f'>>> {full_filename} movido a {path_destination}.')
            return True

        # If I got here, file already exists
        print(f'>>> {full_filename} NO movido, ya existe en {path_destination}.')
        return False

    def configure(self):
        """Public interface. Open the config file in the OS default text editor."""
        def_text_ed = {
            'Linux': 'gnome-text-editor',
            'Windows': 'notepad'}
        result = os.system(def_text_ed[platform.system()] + ' ' + str(self._config.filepath))
        
        if os.waitstatus_to_exitcode(result) != 0:
            print(">>> ERROR! no encuentro un editor de texto para abrir el archivo de configuración")
            print(f">>> Si te sientes valiente, abrilo y editalo a mano. Está en {self._config.filepath}")
