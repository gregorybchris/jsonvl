import json
from pathlib import Path

import pytest

from .constants import CaseSchema, Cases, PyTest


CASES_DIRPATH = Path(__file__).parent / 'cases'


class Case:
    def __init__(self, name, data, schema, result, error, markers):
        self.name = name
        self.data = data
        self.schema = schema
        self.result = result
        self.error = error
        self.markers = markers

    def __repr__(self):
        return "[Case: {}]".format(self.name)


def collect_cases():
    all_cases = []
    for case_dirpath in CASES_DIRPATH.iterdir():
        name = case_dirpath.name

        data_filepath = case_dirpath / Cases.DATA_FILENAME
        with open(data_filepath, 'r') as f:
            data = json.load(f)

        schema_filepath = case_dirpath / Cases.SCHEMA_FILENAME
        with open(schema_filepath, 'r') as f:
            schema = json.load(f)

        meta_filepath = case_dirpath / Cases.META_FILENAME
        with open(meta_filepath, 'r') as f:
            meta = json.load(f)
            if CaseSchema.ERROR not in meta:
                raise ValueError(f"Test case {name} missing \"{CaseSchema.ERROR}\" field at {meta_filepath}")
            if CaseSchema.MARKERS not in meta:
                raise ValueError(f"Test case {name} missing \"{CaseSchema.MARKERS}\" field at {meta_filepath}")
            if CaseSchema.RESULT not in meta:
                raise ValueError(f"Test case {name} missing \"{CaseSchema.RESULT}\" field at {meta_filepath}")

            result = meta[CaseSchema.RESULT]
            error = meta[CaseSchema.ERROR]
            markers = meta[CaseSchema.MARKERS]

        all_cases.append(Case(name, data, schema, result, error, markers))
    return all_cases


@pytest.fixture(params=collect_cases(), ids=lambda x: x.name, scope=PyTest.SESSION)
def case(request):
    request.node.id = request.param.name
    return request.param
