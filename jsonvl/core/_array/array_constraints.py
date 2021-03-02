"""Array constraints."""
from jsonvl._utilities.path_utilities import collect
from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.core.constraint import Constraint
from jsonvl.errors import ErrorMessages, JsonSchemaError, JsonValidationError


class MaxSizeConstraint(Constraint):
    """Maximum array size constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        if not isinstance(constraint_param, int):
            raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                         param=constraint_param, cons=constraint_name, param_types=['integer'])

        array_size = len(data)
        if array_size > constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name, param=constraint_param, data=array_size)


class MinSizeConstraint(Constraint):
    """Minimum array size constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        if not isinstance(constraint_param, int):
            raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                         cons=constraint_name, param=constraint_param, param_types=['integer'])

        array_size = len(data)
        if array_size < constraint_param:
            raise JsonValidationError.create(ErrorMessages.FAILED_CONSTRAINT,
                                             cons=constraint_name, param=constraint_param, data=array_size)


class UniqueConstraint(Constraint):
    """All unique elements constraint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """Constraining method."""
        items = []
        if isinstance(constraint_param, bool):
            items = data
        elif isinstance(constraint_param, str):
            items = collect(data, constraint_param)
        elif isinstance(constraint_param, list):
            for constraint_path in constraint_param:
                self.constrain(constraint_name, data, constraint_path, path)
        else:
            valid_types = [Primitive.BOOLEAN.value, Primitive.STRING.value, Collection.ARRAY.value]
            raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT_PARAM_TYPE,
                                         cons=constraint_name, param_types=valid_types, param=constraint_param)
        for x_i, x in enumerate(items):
            for y_i, y in enumerate(items):
                if x_i != y_i and x == y:
                    raise JsonValidationError.create(ErrorMessages.FAILED_UNIQUE, item=x)
