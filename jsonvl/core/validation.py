"""Convenience functions for default validation."""
import json

from jsonvl.core.validator import Validator


def validate(data, schema):
    """
    Validate JSON data based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    Validator().validate(data, schema)


def validate_file(data_filepath: str, schema_filepath: str):
    """
    Validate a JSON file based on a schema file.

    :param data_filepath: Filepath to JSON data.
    :param schema_filepath: Filepath to JSON schema.
    """
    with open(data_filepath, 'r') as f:
        data = json.load(f)
    with open(schema_filepath, 'r') as f:
        schema = json.load(f)
    Validator().validate(data, schema)
