from jsonvl import Validator
from jsonvl.errors import JsonVlSystemError

import pytest


class TestValidator:
    def test_invalid_primitive_error(self):
        validator = Validator()
        message = ("The system expected a primitive type, but the invalid type could not be parsed. "
                   "Please submit an issue at https://github.com/gregorybchris/jsonvl/issues.")
        with pytest.raises(JsonVlSystemError, match=message):
            validator._validate_primitive_type(type, 'a', 'invalid', {}, 'path-to-data')

    def test_invalid_collection_error(self):
        validator = Validator()
        message = ("The system expected a collection type, but the invalid type could not be parsed. "
                   "Please submit an issue at https://github.com/gregorybchris/jsonvl/issues.")
        with pytest.raises(JsonVlSystemError, match=message):
            validator._validate_collection_type(type, 'a', 'invalid', {}, 'path-to-data')
