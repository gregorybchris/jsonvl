"""Errors messages shown to the user when validating JSON."""


class ErrorMessages:
    """Errors messages shown to the user when validating JSON."""

    # region error-messages

    EXTRA_OBJECT_ATTRS = "Data ({data}) has extra attributes ({extra_attrs}) " \
                         "not defined in the schema ({schema})"
    FAILED_CONSTRAINT = "Failed {cons} ({param}) constraint with value {data}"
    FAILED_PATH_PARSE_ARRAY = "Failed to parse path, use \"@all\" when constructing a path with an array"
    FAILED_PATH_PARSE_TOKEN = "Failed to parse path at token {token}"
    FAILED_TYPE_PARSE = "Could not parse type {type} for data {data}"
    FAILED_UNIQUE = "Unique constraint failed on duplicate item {item}"
    INCORRECT_FORMAT = "Value {data} does not match the {format} format"
    INVALID_CONSTRAINT = "Type {type} does not support the constraint {cons}"
    INVALID_CONSTRAINT_PARAM = "Constraint {cons} requires a parameter " \
                               "of the following types: {param_types}, received {param}"
    MISSING_ARRAY_ELEM = "Array type missing required \"elem\" field"
    MISSING_FORMAT_PATTERN_FIELD = "\"pattern\" field required in format definition at path {path}"
    MISSING_FORMAT_TYPE_FIELD = "\"type\" field required in format definition at path {path}"
    MISSING_OBJECT_ATTRS = "Data ({data}) is missing attributes ({missing_attrs}) " \
                           "defined by the schema ({schema})"
    MISSING_OBJECT_ATTRS_FIELD = "Object types must define all attribute types with an \"attrs\" field"
    MISSING_TYPE_FIELD = "\"type\" field required in type definition at path {path}"
    NOT_OF_TYPE = "Value {data} is not of expected type {type}"
    PARAM_NOT_OF_TYPE = "Parameter {param} for constraint {cons} was not of expected type {type}"
    UNKNOWN_STRING_FORMAT = "Unknown string format {format}, perhaps try a regex format instead"
    UNKNOWN_TYPE = "Unknown type {type}"

    # endregion constants
