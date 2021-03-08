from jsonvl import Constraint, Validator
from jsonvl.errors import CustomConstraintError

import pytest


class MonotoneIncreaseConstraint(Constraint):
    def constrain(self, constraint_name, data, constraint_param, path):
        if len(data) < 2:
            return

        for i in range(1, len(data)):
            if data[i] < data[i - 1]:
                raise ValueError(f"Constraint {constraint_name} failed on elements {data[i]}, {data[i - 1]}")


class UnimplementedConstraint(Constraint):
    pass


class TestCustomConstraints:
    def test_unimplemented(self):
        validator = Validator()
        constraint = UnimplementedConstraint()
        validator.register_constraint(constraint, 'array', 'unimplemented')
        data = [1, 2, 3]
        schema = {'type': 'array', 'elem': 'number', 'cons': {'unimplemented': True}}
        message = "The constraint UnimplementedConstraint was not properly implemented."
        with pytest.raises(CustomConstraintError, match=message):
            validator.validate(data, schema)

    def test_name_conflict(self):
        validator = Validator()
        constraint = UnimplementedConstraint()
        validator.register_constraint(constraint, 'array', 'unimplemented')
        message = "The constraint unimplemented already exists for type array. Please use a different name."
        with pytest.raises(CustomConstraintError, match=message):
            validator.register_constraint(constraint, 'array', 'unimplemented')

    def test_default_name_conflict(self):
        validator = Validator()
        constraint = UnimplementedConstraint()
        message = "The constraint unique already exists for type array. Please use a different name."
        with pytest.raises(CustomConstraintError, match=message):
            validator.register_constraint(constraint, 'array', 'unique')

    def test_custom_pass(self):
        validator = Validator()
        constraint = MonotoneIncreaseConstraint()
        validator.register_constraint(constraint, 'array', 'monotone_inc')
        data = [1, 2, 2, 3]
        schema = {'type': 'array', 'elem': 'number', 'cons': {'monotone_inc': True}}
        validator.validate(data, schema)

    def test_custom_fail(self):
        validator = Validator()
        constraint = MonotoneIncreaseConstraint()
        validator.register_constraint(constraint, 'array', 'monotone_inc')
        data = [1, 3, 3, 2]
        schema = {'type': 'array', 'elem': 'number', 'cons': {'monotone_inc': True}}
        message = "Constraint monotone_inc failed on elements 2, 3"
        with pytest.raises(ValueError, match=message):
            validator.validate(data, schema)

    def test_custom_on_ref_type_fail(self):
        validator = Validator()
        constraint = MonotoneIncreaseConstraint()
        validator.register_constraint(constraint, 'name', 'monotone_inc')
        data = [1, 3, 2]
        schema = {
            'type': '#name',
            'cons': {'monotone_inc': True},
            'defs': {'#name': {'type': 'array', 'elem': 'number'}}
        }
        message = "Constraints are not supported on reference types \\(#name\\)."
        with pytest.raises(ValueError, match=message):
            validator.validate(data, schema)
