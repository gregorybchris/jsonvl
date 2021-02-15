"""Main module for the jsonvl command line interface."""
import argparse

from jsonvl import validate_file


def run():
    """Run the jsonvl CLI."""
    args = _parse_args()

    validate_file(args.data_filepath, args.schema_filepath)


def _parse_args():
    """Parse args required by the jsonvl CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument('data_filepath',
                        help="File path to the JSON data file")
    parser.add_argument('schema_filepath',
                        help="File path to the schema file.")

    return parser.parse_args()
