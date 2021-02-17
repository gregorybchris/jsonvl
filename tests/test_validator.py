from pathlib import Path

import pytest

from jsonvl import validate, validate_file
from jsonvl.errors import JsonValidationError


class TestValidator:
    def test_all_cases(self, case):
        if case.result:
            validate(case.data, case.schema)
        else:
            error_exact_regex = f"^{case.error}$"
            with pytest.raises(JsonValidationError, match=error_exact_regex):
                validate(case.data, case.schema)

    def test_validate_file(self):
        cases_dir = Path(__file__).parent / 'cases'

        case_name = 'number'
        data_filepath = cases_dir / case_name / 'data.json'
        schema_filepath = cases_dir / case_name / 'schema.json'
        validate_file(data_filepath, schema_filepath)
