import os.path
import os
import argparse
import logging
from typing import Tuple
from psd_tools import PSDImage
from PIL import Image

from exporter.base import PhotoshopExporterBase
from exporter.groups_exporter import GroupsExporter


def parse_args() -> Tuple[str, str, bool]:
    """
    Return data passed by a user to the program.

    Returns
    ----------
    str
        Path provided by the user
    bool
        Is the verbose flag passed
    """
    parser = argparse.ArgumentParser(
        description="%(prog)s is a tool for exporting given layers from .psd files into individual .png images",
        epilog=f"It exports from layer groups named: {','.join(GroupsExporter.bases)} and layer groups that start with 'orphan'."
    )
    parser.add_argument(
        '-v', '--verbose', help="report events that occur during program operation", action='store_true',
    )
    parser.add_argument(
        'path',
        help=(
            'Path to a PSD file or a folder. '
            'If the provided path is a folder, program operates on every .psd file in the folder.'
        )
    )
    parser.add_argument(
        'output',
        help=(
            'Output path.'
        )
    )
    args = parser.parse_args()
    inputPath = os.path.abspath(args.path)
    outputPath = os.path.abspath(args.output)
    return inputPath, outputPath, args.verbose,


def set_log_config(isVerbose: bool) -> None:
    """
    Set log config.
    """
    loggingFormat = '%(levelname)s:\t%(message)s'
    if isVerbose:
        logging.basicConfig(format=loggingFormat, level=logging.INFO)
    else:
        logging.basicConfig(format=loggingFormat, level=logging.WARNING)


if __name__ == '__main__':
    input_path, output_path, isVerbose = parse_args()
    set_log_config(isVerbose)
    exporter = GroupsExporter(input_path, output_path=output_path, verbose=isVerbose)
    exporter.export()
