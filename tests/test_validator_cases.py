from pathlib import Path

from jsonvl import validate, validate_file
from jsonvl.errors import JsonSchemaError, JsonValidationError

import pytest
import re

from .constants import Cases


class TestValidatorCases:
    def test_all_cases(self, case):
        if case.result:
            validate(case.data, case.schema)
        else:
            escaped_error_regex = re.escape(f"{case.error}")
            error_exact_regex = f"^{escaped_error_regex}$"
            if case.error_type == Cases.DATA_ERROR:
                with pytest.raises(JsonValidationError, match=error_exact_regex):
                    validate(case.data, case.schema)
            elif case.error_type == Cases.SCHEMA_ERROR:
                with pytest.raises(JsonSchemaError, match=error_exact_regex):
                    validate(case.data, case.schema)
            else:
                raise ValueError(f"Test case {case.name} has invalid \"{Cases.ERROR_TYPE}\" "
                                 f"field at {case.meta_filepath}")

    def test_validate_file(self):
        cases_dir = Path(__file__).parent / 'cases'

        case_group = 'number'
        case_name = 'number'
        data_filepath = cases_dir / case_group / case_name / 'data.json'
        schema_filepath = cases_dir / case_group / case_name / 'schema.json'
        validate_file(data_filepath, schema_filepath)

    def test_validate_file_fail(self):
        cases_dir = Path(__file__).parent / 'cases'

        case_group = 'number'
        case_name = 'number_fail'
        data_filepath = cases_dir / case_group / case_name / 'data.json'
        schema_filepath = cases_dir / case_group / case_name / 'schema.json'
        message = r'^Value 4 is not of expected type number at path root$'
        with pytest.raises(JsonValidationError, match=message):
            validate_file(data_filepath, schema_filepath)
