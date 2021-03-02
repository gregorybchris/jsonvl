import inspect

import pytest

from jsonvl.errors import ErrorMessages

from ..constants import PyTest


REGION_DATA_ERRORS = 'data-errors'
REGION_SCHEMA_ERRORS = 'schema-errors'
REGION_SYSTEM_ERRORS = 'system-errors'
REGION_CUSTOM_CONSTRAINT_ERRORS = 'custom-constraint-errors'


class TestErrorMessages:
    @pytest.fixture(params=[
        REGION_DATA_ERRORS,
        REGION_SCHEMA_ERRORS,
        REGION_SYSTEM_ERRORS,
        REGION_CUSTOM_CONSTRAINT_ERRORS,
    ], scope=PyTest.SESSION)
    def region_name(self, request):
        return request.param

    def test_error_messages_ordered(self, region_name):
        region_start = f"# region {region_name}"
        region_end = "endregion"

        file_path = inspect.getfile(ErrorMessages().__class__)
        with open(file_path) as f:
            line = f.readline()
            while region_start not in line:
                line = f.readline()

            prev = ""
            while region_end not in line:
                line = f.readline()
                try:
                    if line.strip().startswith("\""):
                        continue
                    curr = line[:line.index('=')].strip()
                except ValueError:
                    continue

                assert prev < curr, f"Constants {prev} and {curr} are out of order"
                prev = curr
