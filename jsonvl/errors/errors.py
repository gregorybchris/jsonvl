"""Exceptions raised when validating JSON."""


class JsonValidationError(ValueError):
    """ValidationError type raised when validation fails."""

    @classmethod
    def create(cls, message_format, **kwargs):
        """
        Create a new error based on a message format.

        :param message_format: Message format to raise.
        :param kwargs: Keyword arguments to inject into the message format.
        """
        return cls(message_format.format(**kwargs))
