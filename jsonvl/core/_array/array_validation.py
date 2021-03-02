"""Array validation."""
from jsonvl.constants.builtins import Collection
from jsonvl.constants.reserved import ReservedWords
from jsonvl.core._array import array_constraints
from jsonvl.core._array.array_constraint_names import ArrayConstraintNames
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


TYPE_NAME = Collection.ARRAY.value


def validate_array(data, schema, defs, path, validator):
    """
    Validate a JSON array based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, list):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if ReservedWords.ELEMENT not in schema:
        raise JsonSchemaError.create(ErrorMessages.MISSING_ARRAY_ELEM)

    elem_schema = schema[ReservedWords.ELEMENT]
    for i, elem in enumerate(data):
        new_path = f'{path}[{i}]'
        validator._validate(elem, elem_schema, defs, new_path)

    if ReservedWords.CONSTRAINTS in schema:
        validator._validate_constraints(data, TYPE_NAME, schema[ReservedWords.CONSTRAINTS], path)


def register_array_constraints(validator):
    """
    Register default array constraints.

    :param validator: jsonvl.Validator instance on which to register the constraints.
    """
    validator.register_constraint(array_constraints.MaxSizeConstraint(),
                                  TYPE_NAME, ArrayConstraintNames.MAX_SIZE.value)
    validator.register_constraint(array_constraints.MinSizeConstraint(),
                                  TYPE_NAME, ArrayConstraintNames.MIN_SIZE.value)
    validator.register_constraint(array_constraints.UniqueConstraint(),
                                  TYPE_NAME, ArrayConstraintNames.UNIQUE.value)
