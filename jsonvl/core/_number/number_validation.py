"""String validation."""
from jsonvl.constants.builtins import Primitive
from jsonvl.constants.reserved import Reserved
from jsonvl.core._number.number_constraints import NumberConstraints
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


TYPE_NAME = Primitive.NUMBER.value


def validate_number(data, schema, defs, path):
    """
    Validate a JSON number based on a schema.

    :param data: JSON data as a Python object.
    :param schema: JSON schema as a Python object.
    """
    if not isinstance(data, (int, float)):
        raise JsonValidationError.create(ErrorMessages.NOT_OF_TYPE, data=data, type=TYPE_NAME)

    if isinstance(schema, str):
        return

    if Reserved.CONSTRAINTS in schema:
        type_constraints = schema[Reserved.CONSTRAINTS]
        for cons_name, cons_param in type_constraints.items():
            if not NumberConstraints.has(cons_name):
                raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT,
                                             type=TYPE_NAME, cons=cons_name)

            if cons_name == NumberConstraints.LT.value:
                _constrain_lt(cons_name, data, cons_param, path)
            elif cons_name == NumberConstraints.GT.value:
                _constrain_gt(cons_name, data, cons_param, path)
            elif cons_name == NumberConstraints.LTE.value:
                _constrain_lte(cons_name, data, cons_param, path)
            elif cons_name == NumberConstraints.GTE.value:
                _constrain_gte(cons_name, data, cons_param, path)
            elif cons_name == NumberConstraints.EQ.value:
                _constrain_eq(cons_name, data, cons_param, path)
            else:
                raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT,
                                             type=TYPE_NAME, cons=cons_name)


def _check_type(cons_name, cons_param):
    if not isinstance(cons_param, (int, float)):
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     cons=cons_name, param_types=[Primitive.NUMBER.value], param=cons_param)


def _constrain_lt(cons_name, data, cons_param, path):
    _check_type(cons_name, cons_param)
    if data >= cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=data)


def _constrain_gt(cons_name, data, cons_param, path):
    _check_type(cons_name, cons_param)
    if data <= cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=data)


def _constrain_lte(cons_name, data, cons_param, path):
    _check_type(cons_name, cons_param)
    if data > cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=data)


def _constrain_gte(cons_name, data, cons_param, path):
    _check_type(cons_name, cons_param)
    if data < cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=data)


def _constrain_eq(cons_name, data, cons_param, path):
    _check_type(cons_name, cons_param)
    if data != cons_param:
        raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                         cons=cons_name, param=cons_param, data=data)
