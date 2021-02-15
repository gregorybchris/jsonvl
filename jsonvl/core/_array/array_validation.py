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
        for cons_name, cons_value in type_constraints.items():
            if not ArrayConstraints.has(cons_name):
                raise ValidationError(f"The type {TYPE_NAME} has no constraint {cons_name}")

            if cons_name == ArrayConstraints.UNIQUE.value:
                _constrain_unique(cons_name, data, cons_value, path)
            else:
                raise ValidationError(f"The constraint {cons_name} is not implemented for type {TYPE_NAME}")


def _constrain_unique(cons_name, data, cons_value, path):
    items = []
    if isinstance(cons_value, bool):
        items = data
    elif isinstance(cons_value, str):
        items = collect(data, cons_value)
    elif isinstance(cons_value, list):
        for cons_path in cons_value:
            _constrain_unique(cons_name, data, cons_path, path)
    else:
        raise ValidationError(f"The {cons_name} constraint value ({cons_value}) "
                              f"for the data {data} must be of "
                              f"{Primitive.BOOLEAN.value}, "
                              f"{Primitive.STRING.value}, or "
                              f"{Collection.ARRAY.value} type")

    for x_i, x in enumerate(items):
        for y_i, y in enumerate(items):
            if x_i != y_i and x == y:
                raise ValidationError(f"Constraint \"{cons_name}\" was not met with "
                                      f"duplicate item {x}")
