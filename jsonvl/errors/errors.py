"""Exceptions raised when validating JSON."""


class JsonVlError(ValueError):
    """JsonVlError type raised when validation fails."""

    pass


class JsonValidationError(JsonVlError):
    """JsonValidationError type raised when validation fails with malformed JSON."""

    @classmethod
    def create(cls, message_format, **kwargs):
        """
        Create a new error based on a message format.

        :param message_format: Message format to raise.
        :param kwargs: Keyword arguments to inject into the message format.
        """
        return cls(message_format.format(**kwargs))


class JsonSchemaError(JsonVlError):
    """JsonSchemaError type raised when validation fails with an invalid JSON schema."""

    @classmethod
    def create(cls, message_format, **kwargs):
        """
        Create a new error based on a message format.

        :param message_format: Message format to raise.
        :param kwargs: Keyword arguments to inject into the message format.
        """
        return cls(message_format.format(**kwargs))
