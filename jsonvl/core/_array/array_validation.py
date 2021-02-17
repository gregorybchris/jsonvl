"""Array validation."""
from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.constants.reserved import Reserved
from jsonvl.core._array.array_constraints import ArrayConstraints
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError
from jsonvl.utilities.path_utilities import collect


TYPE_NAME = Collection.ARRAY.value


def validate_array(data, schema, defs, path, validator):
    """
    Validate a JSON array based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, list):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if Reserved.ELEMENT not in schema:
        raise JsonValidationError.create(ErrorMessages.MISSING_ARRAY_ELEM)

    elem_schema = schema[Reserved.ELEMENT]
    for i, elem in enumerate(data):
        new_path = f'{path}[{i}]'
        validator._validate(elem, elem_schema, defs, new_path)

    if Reserved.CONSTRAINTS in schema:
        type_constraints = schema[Reserved.CONSTRAINTS]
        for cons_name, cons_param in type_constraints.items():
            if not ArrayConstraints.has(cons_name):
                raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT, type=TYPE_NAME, cons=cons_name)

            if cons_name == ArrayConstraints.MAX_SIZE.value:
                _constrain_max_size(cons_name, data, cons_param, path)
            elif cons_name == ArrayConstraints.MIN_SIZE.value:
                _constrain_min_size(cons_name, data, cons_param, path)
            elif cons_name == ArrayConstraints.UNIQUE.value:
                _constrain_unique(cons_name, data, cons_param, path)
            else:
                raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT, type=TYPE_NAME, cons=cons_name)


def _constrain_unique(cons_name, data, cons_param, path):
    items = []
    if isinstance(cons_param, bool):
        items = data
    elif isinstance(cons_param, str):
        items = collect(data, cons_param)
    elif isinstance(cons_param, list):
        for cons_path in cons_param:
            _constrain_unique(cons_name, data, cons_path, path)
    else:
        valid_types = [Primitive.BOOLEAN.value, Primitive.STRING.value, Collection.ARRAY.value]
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     cons=cons_name, param_types=valid_types, param=cons_param)
    for x_i, x in enumerate(items):
        for y_i, y in enumerate(items):
            if x_i != y_i and x == y:
                raise JsonValidationError.create(ErrorMessages.FAILED_UNIQUE, item=x)


def _constrain_max_size(cons_name, data, cons_param, path):
    if not isinstance(cons_param, int):
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     param=cons_param, cons=cons_name, param_types=['integer'])

    array_size = len(data)
    if array_size > cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=array_size)


def _constrain_min_size(cons_name, data, cons_param, path):
    if not isinstance(cons_param, int):
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     cons=cons_name, param=cons_param, param_types=['integer'])

    array_size = len(data)
    if array_size < cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=array_size)
