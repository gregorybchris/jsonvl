from pathlib import Path

import pytest

from jsonvl import validate_file


EXAMPLES_DIRPATH = Path(__file__).parent / '..' / 'examples'
DATA_FILENAME = 'data.json'
SCHEMA_FILENAME = 'schema.json'


def get_examples():
    all_examples = []
    for example_dirpath in EXAMPLES_DIRPATH.iterdir():
        if example_dirpath.is_dir():
            data_filepath = example_dirpath / DATA_FILENAME
            schema_filepath = example_dirpath / SCHEMA_FILENAME
            all_examples.append((example_dirpath, data_filepath, schema_filepath))
    return all_examples


class TestExamples:
    @pytest.fixture(params=get_examples(), ids=lambda x: x[0])
    def example(self, request):
        return request.param

    def test_all_examples(self, example):
        _, data_filepath, schema_filepath = example
        validate_file(data_filepath, schema_filepath)
