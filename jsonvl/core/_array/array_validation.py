"""Array validation."""
from jsonvl.constants.reserved import Reserved
from jsonvl.constants.builtins import Primitive, Collection
from jsonvl.core._array.array_constraints import ArrayConstraints
from jsonvl.exceptions.errors import ValidationError
from jsonvl.utilities.path_utilities import collect


TYPE_NAME = Collection.ARRAY.value


def validate_array(data, schema, validator, path):
    """
    Validate a JSON array based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, list):
        raise ValidationError(f"Expected {data} to be an array")

    if Reserved.ELEMENT not in schema:
        raise ValidationError("Array types must define the element type with the \"elem\" field")

    elem_schema = schema[Reserved.ELEMENT]
    for i, elem in enumerate(data):
        new_path = f'{path}[{i}]'
        validator._validate(elem, elem_schema, new_path)

    if Reserved.CONSTRAINTS in schema:
        type_constraints = schema[Reserved.CONSTRAINTS]
        for cons_name, cons_param in type_constraints.items():
            if not ArrayConstraints.has(cons_name):
                raise ValidationError(f"The type {TYPE_NAME} has no constraint {cons_name}")

            if cons_name == ArrayConstraints.MAX_SIZE.value:
                _constrain_max_size(cons_name, data, cons_param, path)
            elif cons_name == ArrayConstraints.MIN_SIZE.value:
                _constrain_min_size(cons_name, data, cons_param, path)
            elif cons_name == ArrayConstraints.UNIQUE.value:
                _constrain_unique(cons_name, data, cons_param, path)
            else:
                raise ValidationError(f"The constraint {cons_name} is not implemented for type {TYPE_NAME}")


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
        raise ValidationError(f"The {cons_name} constraint value ({cons_param}) "
                              f"for the data {data} must be of "
                              f"{Primitive.BOOLEAN.value}, "
                              f"{Primitive.STRING.value}, or "
                              f"{Collection.ARRAY.value} type")

    for x_i, x in enumerate(items):
        for y_i, y in enumerate(items):
            if x_i != y_i and x == y:
                raise ValidationError(f"Constraint \"{cons_name}\" was not met with "
                                      f"duplicate item {x}")


def _constrain_max_size(cons_name, data, cons_param, path):
    if not isinstance(cons_param, int):
        raise ValidationError(f"Expected \"{cons_name}\" param ({cons_param}) to be an integer")

    array_size = len(data)
    if array_size > cons_param:
        raise ValidationError(f"Constraint \"{cons_name}\" ({cons_param}) was not met with array size {array_size}")


def _constrain_min_size(cons_name, data, cons_param, path):
    if not isinstance(cons_param, int):
        raise ValidationError(f"Expected \"{cons_name}\" param ({cons_param}) to be an integer")

    array_size = len(data)
    if array_size < cons_param:
        raise ValidationError(f"Constraint \"{cons_name}\" ({cons_param}) was not met with array size {array_size}")
