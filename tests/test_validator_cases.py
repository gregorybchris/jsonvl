from pathlib import Path

from jsonvl import validate, validate_file
from jsonvl.errors import JsonSchemaError, JsonValidationError

import pytest

from .constants import Cases


class TestValidatorCases:
    def test_all_cases(self, case):
        if case.result:
            validate(case.data, case.schema)
        else:
            error_exact_regex = f"^{case.error}$"
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

        case_name = 'number'
        data_filepath = cases_dir / case_name / 'data.json'
        schema_filepath = cases_dir / case_name / 'schema.json'
        validate_file(data_filepath, schema_filepath)
