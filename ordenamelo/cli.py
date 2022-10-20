"""This module provides the ordenamelo CLI."""

import argparse

from ordenamelo import __version__
from ordenamelo.organizer import Organizer


def parse_cmd_line_arguments():
    """Return the parsed cmd line arguments."""
    parser = argparse.ArgumentParser(
        prog="ordenamelo",
        description="Para renombrar y mover esos odiosos comprobantes de pago mensuales!",
        epilog="Todo en orden! (╯°□°)╯",
    )
    parser.version = __version__

    parser.add_argument("-v", "--version", action="version")
    parser.add_argument("-ro", "--rename-only", action="store_true",
                             help="Renombrar archivos sin mover")
    parser.add_argument("-c", "--config", action="store_true",
                             help="Ver/configurar rutas, reglas y/o palabras clave.")

    return parser.parse_args()


def main():
    """Main function, directs execution of the program."""
    args = parse_cmd_line_arguments()
    organizer = Organizer()
    if args.config:
        organizer.configure()
    else:
        organizer.organize(rename_only=args.rename_only)


if __name__ == '__main__':
    main()
