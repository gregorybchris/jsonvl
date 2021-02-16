import pytest

from pathlib import Path

from jsonvl import validate, validate_file
from jsonvl.errors import JsonValidationError

from .constants import CaseSchema


class TestValidator:
    def test_all_cases(self, case):
        if case.expect[CaseSchema.RESULT]:
            validate(case.data, case.schema)
        else:
            if CaseSchema.ERROR not in case.expect:
                raise ValueError("Test case missing error message")
            with pytest.raises(JsonValidationError, match=case.expect[CaseSchema.ERROR]):
                validate(case.data, case.schema)

    def test_validate_file(self):
        cases_dir = Path(__file__).parent / 'cases'

        case_name = 'number'
        data_filepath = cases_dir / case_name / 'data.json'
        schema_filepath = cases_dir / case_name / 'schema.json'
        validate_file(data_filepath, schema_filepath)
