"""Number constraints."""
from jsonvl.constants.builtins import Primitive
from jsonvl.core.constraint import Constraint
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


class LtConstraint(Constraint):
    """Less than constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        _check_number_type(constraint_name, constraint_param)
        if data >= constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name,
                                             param=constraint_param,
                                             data=data)


class GtConstraint(Constraint):
    """Greater than constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        _check_number_type(constraint_name, constraint_param)
        if data <= constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name,
                                             param=constraint_param,
                                             data=data)


class LteConstraint(Constraint):
    """Less than or equal to constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        _check_number_type(constraint_name, constraint_param)
        if data > constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name,
                                             param=constraint_param,
                                             data=data)


class GteConstraint(Constraint):
    """Greater than or equal to constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        _check_number_type(constraint_name, constraint_param)
        if data < constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name,
                                             param=constraint_param,
                                             data=data)


class EqConstraint(Constraint):
    """Equal to constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        _check_number_type(constraint_name, constraint_param)
        if data != constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name,
                                             param=constraint_param,
                                             data=data)


def _check_number_type(constraint_name, constraint_param):
    if not isinstance(constraint_param, (int, float)):
        raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                     cons=constraint_name,
                                     param_types=[Primitive.NUMBER.value],
                                     param=constraint_param)
