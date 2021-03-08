import json
import re
from pathlib import Path

import pytest

from .constants import Cases, PyTest


CASES_DIRPATH = Path(__file__).parent / 'cases'


class Case:
    def __init__(self, name, data, schema, meta_filepath,
                 result=True, error=None, error_type=None, markers=None):
        self.name = name
        self.data = data
        self.schema = schema
        self.meta_filepath = meta_filepath
        self.result = result
        self.error = error
        self.error_type = error_type
        self.markers = markers

    def __repr__(self):
        return "[Case: {}]".format(self.name)


def collect_cases():
    all_cases = []
    for case_group_dirpath in CASES_DIRPATH.iterdir():
        for case_dirpath in case_group_dirpath.iterdir():
            validate_case_dirpath(case_dirpath)

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

            validate_meta(meta, meta_filepath, name)

            all_cases.append(Case(name, data, schema, meta_filepath, **meta))
    return all_cases


def validate_case_dirpath(case_dirpath):
    if not re.match(r'^[a-z_]{3,40}$', case_dirpath.name):
        raise ValueError(f"Invalid case directory name {case_dirpath.name}")


def validate_meta(meta, meta_filepath, name):
    if Cases.RESULT not in meta:
        raise ValueError(f"Test case {name} missing \"{Cases.RESULT}\" field at {meta_filepath}")

    if meta[Cases.RESULT]:
        for field in [Cases.ERROR, Cases.ERROR_TYPE]:
            if field in meta and meta[field] is not None:
                raise ValueError(f"Test case {name} has unexpected \"{field}\" field at {meta_filepath}")
    else:
        for field in [Cases.ERROR, Cases.ERROR_TYPE]:
            if field not in meta or meta[field] is None:
                raise ValueError(f"Test case {name} missing required \"{field}\" field at {meta_filepath}")


@pytest.fixture(params=collect_cases(), ids=lambda x: x.name, scope=PyTest.SESSION)
def case(request):
    request.node.id = request.param.name
    return request.param
