"""Utilities for parsing JSON paths."""
import itertools
import re

from jsonvl.constants.reserved import Reserved
from jsonvl.exceptions.errors import ValidationError


def collect(data, path):
    """
    Collect all items from a JSON document that match the given path.

    :param data: JSON data to parse.
    :param path: Path through the data to the collected elements.
    :return: List of JSON data elements that match the given path.
    """
    path_tokens = _parse_path(path)
    return _collect(data, path_tokens)


def _collect(data, path_tokens):
    if len(path_tokens) == 0:
        return [data]

    token = path_tokens[0]
    if isinstance(data, list):
        if token != Reserved.ALL:
            raise ValidationError("Failed to collect items from path when parsing array type, use \"@all\"")

        lists_collected = [_collect(value, path_tokens[1:]) for value in data]
        return list(itertools.chain.from_iterable(lists_collected))
    elif isinstance(data, dict):
        if token not in data:
            raise ValidationError(f"Failed to parse path at token {token}")

        return _collect(data[token], path_tokens[1:])
    else:
        raise ValidationError(f"Failed to parse path at token {token}")


def _parse_path(path):
    return [token for token in re.split(r'(?<!\\)\.|(?<!\\)@', path) if token != '']
