"""Errors messages shown to the user when validating JSON."""


class ErrorMessages:
    """Errors messages shown to the user when validating JSON."""

    # region data-errors

    EXTRA_OBJECT_ATTR = "Data ({data}) has extra attributes ({extra_attr}) " \
                        "not defined in the schema ({schema})"
    FAILED_CONSTRAINT = "Failed {cons} ({param}) constraint with value {data}"
    FAILED_UNION_TYPE_PARSE = "Could not parse value {data} as union type {types}"
    FAILED_UNIQUE = "Unique constraint failed on duplicate item {item}"
    INCORRECT_FORMAT = "Value {data} does not match the {format} format"
    MISSING_OBJECT_ATTR = "Data ({data}) is missing attributes ({missing_attr}) " \
                          "defined by the schema ({schema})"
    NOT_OF_TYPE = "Value {data} is not of expected type {type}"

    # endregion

    # region schema-errors

    FAILED_PATH_PARSE_ARRAY = "Failed to parse path, use \"@all\" when constructing a path with an array"
    FAILED_PATH_PARSE_TOKEN = "Failed to parse path at token {token}"
    FAILED_SCHEMA_TYPE_PARSE = "Could not parse schema type {type}"
    INVALID_CONSTRAINT = "Type {type} does not support the constraint {cons}"
    INVALID_CONSTRAINT_PARAM_TYPE = "Constraint {cons} requires a parameter " \
                                    "of the following types: {param_types}, received {param}"
    MISSING_ARRAY_ELEM = "Array type missing required \"elem\" field"
    MISSING_FORMAT_PATTERN_FIELD = "\"pattern\" field required in format definition at path {path}"
    MISSING_FORMAT_TYPE_FIELD = "\"type\" field required in format definition at path {path}"
    MISSING_OBJECT_ATTR_FIELD = "Object types must define all attribute types with an \"attr\" field"
    MISSING_TYPE_FIELD = "\"type\" field required in type definition at path {path}"
    RECURSIVE_SCHEMA_REFERENCE = "Recursive schema references are not allowed, please update {ref}"
    REFERENCE_NOT_FOUND = "Could not find the definition {ref}"
    UNKNOWN_STRING_FORMAT = "Unknown string format {format}, perhaps try a regex format instead"
    UNKNOWN_TYPE = "Unknown type {type}"

    # endregion
