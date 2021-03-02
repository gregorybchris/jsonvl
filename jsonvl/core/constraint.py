"""JSON validator type constaint."""
from abc import ABC

from jsonvl.errors import CustomConstraintError, ErrorMessages


class Constraint(ABC):
    """JSON validator type constaint."""

    def constrain(self, constraint_name, data, constraint_param, path):
        """
        Apply a constraint to the given JSON data.

        :param constraint_name: Name of the constraint to be applied.
        :param data: Data to which the constraint should be applied.
        :param constraint_param: A parameter passed to the constraint.
        """
        class_name = self.__class__.__name__
        raise CustomConstraintError.create(ErrorMessages.UNIMPLEMENTED_CONSTRAINT, name=class_name)
