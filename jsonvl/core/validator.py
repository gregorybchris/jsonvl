"""JSON validator."""
from copy import deepcopy

from jsonvl.constants.builtins import Collection, Primitive
from jsonvl.constants.reserved import ReservedSymbols, ReservedWords
from jsonvl.core._array.array_validation import register_array_constraints, validate_array
from jsonvl.core._boolean.boolean_validation import register_boolean_constraints, validate_boolean
from jsonvl.core._null.null_validation import register_null_constraints, validate_null
from jsonvl.core._number.number_validation import register_number_constraints, validate_number
from jsonvl.core._object.object_validation import register_object_constraints, validate_object
from jsonvl.core._string.string_validation import register_string_constraints, validate_string
from jsonvl.errors import (CustomConstraintError,
                           ErrorMessages, JsonSchemaError,
                           JsonValidationError, JsonVlSystemError)


class Validator:
    """JSON validator."""

    def __init__(self):
        """Construct a new Validator."""
        self._constraints = {}
        self._register_default_constraints()

    def _register_default_constraints(self):
        register_array_constraints(self)
        register_boolean_constraints(self)
        register_null_constraints(self)
        register_number_constraints(self)
        register_object_constraints(self)
        register_string_constraints(self)

    def validate(self, data, schema):
        """
        Validate JSON data based on a schema.

        :param data: JSON data as a Python object.
        :param schema: JSON schema as a Python object.
        """
        self._validate(data, schema, defs={}, path='json')

    def register_constraint(self, constraint, type, name):
        """
        Register a new custom constraint on the Validator.

        :param constraint: Instance of the jsonvl.Constraint class.
        :param type: The type for which the constraint will be applied.
            Currently only builtin JSON types are supported.
        :param name: The name of the constraint. The value used in the schema to apply the constraint.
        """
        if type not in self._constraints:
            self._constraints[type] = {}

        if name in self._constraints[type]:
            raise CustomConstraintError.create(ErrorMessages.DUPLICATE_CONSTRAINT_NAME, cons=name, type=type)

        self._constraints[type][name] = constraint

    def get_constraint(self, type, name):
        """
        Retrieve a custom constraint from the Validator.

        :param type: The type for which the constraint will be applied.
            Currently only builtin JSON types are supported.
        :param name: The name of the constraint. The value used in the schema to apply the constraint.
        :return: Instance of the jsonvl.Constraint class.
        """
        if type not in self._constraints:
            return None
        if name not in self._constraints[type]:
            return None
        return self._constraints[type][name]

    def _validate(self, data, schema, defs, path):
        if isinstance(schema, str):
            self._validate_str_schema(data, schema, defs, path)
        elif isinstance(schema, list):
            self._validate_list_schema(data, schema, defs, path)
        elif isinstance(schema, dict):
            self._validate_dict_schema(data, schema, defs, path)
        else:
            raise JsonSchemaError.create(ErrorMessages.FAILED_SCHEMA_TYPE_PARSE, type=schema)

    def _validate_str_schema(self, data, type, defs, path):
        if type.startswith(ReservedSymbols.REF):
            ref = type
            if ref in defs:
                ref_schema = defs[ref]
                self._validate(data, ref_schema, defs, path)
                return
            else:
                raise JsonSchemaError.create(ErrorMessages.REFERENCE_NOT_FOUND, ref=ref)

        if Primitive.has(type):
            self._validate_primitive_type(type, data, type, defs, path)
        elif Collection.has(type):
            raise JsonSchemaError.create(ErrorMessages.INVALID_COLLECTION_SCHEMA, type=type)
        else:
            raise JsonSchemaError.create(ErrorMessages.UNKNOWN_TYPE, type=type)

    def _validate_list_schema(self, data, schema, defs, path):
        union_schemas = schema
        successful_schema = None
        for union_schema in union_schemas:
            try:
                self._validate(data, union_schema, defs, path)
                successful_schema = union_schema
                break
            except JsonValidationError:
                pass
        if successful_schema is None:
            raise JsonValidationError.create(ErrorMessages.FAILED_UNION_TYPE_PARSE, data=data, types=union_schemas)

    def _validate_dict_schema(self, data, schema, defs, path):
        if ReservedWords.TYPE not in schema:
            raise JsonSchemaError.create(ErrorMessages.MISSING_TYPE_FIELD, path=path)

        if ReservedWords.DEFS in schema:
            defs = deepcopy(defs)
            defs.update(schema[ReservedWords.DEFS])

        type = schema[ReservedWords.TYPE]

        if type in defs:
            self._validate(data, type, defs, path)

            if ReservedWords.CONSTRAINTS in schema:
                raise JsonSchemaError.create(ErrorMessages.INVALID_REFERENCE_TYPE_CONSTRAINT, type=type)

            return

        if Primitive.has(type):
            self._validate_primitive_type(type, data, schema, defs, path)
        elif Collection.has(type):
            self._validate_collection_type(type, data, schema, defs, path)
        else:
            raise JsonSchemaError.create(ErrorMessages.UNKNOWN_TYPE, type=type)

    def _validate_primitive_type(self, type, data, schema, defs, path):
        if type == Primitive.BOOLEAN.value:
            validate_boolean(data, schema, defs, path, self)
        elif type == Primitive.NULL.value:
            validate_null(data, schema, defs, path, self)
        elif type == Primitive.NUMBER.value:
            validate_number(data, schema, defs, path, self)
        elif type == Primitive.STRING.value:
            validate_string(data, schema, defs, path, self)
        else:
            raise JsonVlSystemError.create(ErrorMessages.UNEXPECTED_PRIMITIVE_TYPE, type=schema)

    def _validate_collection_type(self, type, data, schema, defs, path):
        if type == Collection.ARRAY.value:
            validate_array(data, schema, defs, path, self)
        elif type == Collection.OBJECT.value:
            validate_object(data, schema, defs, path, self)
        else:
            raise JsonVlSystemError.create(ErrorMessages.UNEXPECTED_COLLECTION_TYPE, type=schema)

    def _validate_constraints(self, data, type, constraints, path):
        for cons_name, cons_param in constraints.items():
            constraint = self.get_constraint(type, cons_name)

            if constraint is None:
                raise JsonSchemaError.create(ErrorMessages.INVALID_CONSTRAINT, type=type, cons=cons_name)

            constraint.constrain(cons_name, data, cons_param, path)
