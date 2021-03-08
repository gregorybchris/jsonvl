"""Object validation."""
from jsonvl.constants.builtins import Collection
from jsonvl.constants.reserved import ReservedWords
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


TYPE_NAME = Collection.OBJECT.value


def validate_object(data, schema, defs, path, validator):
    """
    Validate a JSON object based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, dict):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME, path=path)

    if ReservedWords.ATTRIBUTES not in schema:
        raise JsonSchemaError.create(ErrorMessages.MISSING_OBJECT_ATTR_FIELD)

    attr_schema = schema[ReservedWords.ATTRIBUTES]

    missing_attr_data = attr_schema.keys() - data.keys()
    if len(missing_attr_data) != 0:
        raise JsonValidationError.create(ErrorMessages.MISSING_OBJECT_ATTR,
                                         data=data, missing_attr=missing_attr_data, schema=attr_schema)

    missing_attr_schema = data.keys() - attr_schema.keys()
    if len(missing_attr_schema) != 0:
        raise JsonValidationError.create(ErrorMessages.EXTRA_OBJECT_ATTR,
                                         data=data, extra_attr=missing_attr_schema, schema=attr_schema)

    for attr, attr_type in attr_schema.items():
        new_path = f'{path}.{attr}'
        validator._validate(data[attr], attr_type, defs, new_path)

    if ReservedWords.CONSTRAINTS in schema:
        validator._validate_constraints(data, TYPE_NAME, schema[ReservedWords.CONSTRAINTS], path)


def register_object_constraints(validator):
    """
    Register default object constraints.

    :param validator: jsonvl.Validator instance on which to register the constraints.
    """
    pass
