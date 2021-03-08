"""Utilities for parsing JSON paths."""
import itertools
import re

from jsonvl.constants.reserved import ReservedWords
from jsonvl.errors import ErrorMessages, JsonSchemaError


def collect(data, path):
    """
    Collect all items from a JSON document that match the given path.

    :param data: JSON data to parse.
    :param path: Path through the data to the collected elements.
    :return: List of JSON data elements that match the given path.
    """
    path_tokens = re.split(r'(?<!\\)\.|(?<!\\)@', path)
    path_tokens = [token.replace('\\', '') for token in path_tokens if token != '']
    return _collect(data, path_tokens, path)


def _collect(data, path_tokens, path):
    if len(path_tokens) == 0:
        return [data]

    token = path_tokens[0]
    if isinstance(data, list):
        if token != ReservedWords.ALL:
            raise JsonSchemaError.create(ErrorMessages.FAILED_PATH_PARSE_ARRAY)

        lists_collected = [_collect(value, path_tokens[1:], path) for value in data]
        return list(itertools.chain.from_iterable(lists_collected))
    elif isinstance(data, dict):
        if token not in data:
            raise JsonSchemaError.create(ErrorMessages.FAILED_PATH_PARSE_TOKEN, token=token, path=path)

        return _collect(data[token], path_tokens[1:], path)
    else:
        raise JsonSchemaError.create(ErrorMessages.FAILED_PATH_PARSE_TOKEN, token=token, path=path)
