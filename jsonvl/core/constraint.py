"""JSON validator type constaint."""
from abc import ABC

from jsonvl._path.path_utilities import query
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

    def query(self, data, path):
        """
        Collect all items in the data that match the given path.

        :param data: Data from which to collect items.
        :param path: Path in data from which to collect items.
        :return: A list of items from the data matching the path.
        """
        return query(data, path)
