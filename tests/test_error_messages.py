import inspect
import pytest

from jsonvl.errors import ErrorMessages

from .constants import PyTest


REGION_ERROR_MESSAGES = 'error-messages'


class TestErrorMessages:
    @pytest.fixture(params=[
        REGION_ERROR_MESSAGES
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
