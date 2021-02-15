import json
import pytest

from pathlib import Path

from .constants import PyTest, Cases


CASES_DIRPATH = Path(__file__).parent / 'cases'


class Case:
    def __init__(self, name, data, schema, expect):
        self.name = name
        self.data = data
        self.schema = schema
        self.expect = expect

    def __repr__(self):
        return "[Case: {}]".format(self.name)


def collect_cases():
    all_cases = []
    for case_dirpath in CASES_DIRPATH.iterdir():
        name = case_dirpath.name
        with open(case_dirpath / Cases.DATA_FILENAME, 'r') as f:
            data = json.load(f)
        with open(case_dirpath / Cases.SCHEMA_FILENAME, 'r') as f:
            schema = json.load(f)
        with open(case_dirpath / Cases.EXPECT_FILENAME, 'r') as f:
            expect = json.load(f)
        all_cases.append(Case(name, data, schema, expect))
    return all_cases


@pytest.fixture(params=collect_cases(), ids=lambda x: x.name, scope=PyTest.SESSION)
def case(request):
    request.node.id = request.param.name
    return request.param
