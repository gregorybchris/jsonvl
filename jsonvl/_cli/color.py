"""Color printing."""


class Color:
    """Terminal colors."""

    BLUE = '\x1b[34m'
    CYAN = '\x1b[36m'
    GREEN = '\x1b[32m'
    ORANGE = '\x1b[33m'
    RED = '\x1b[31m'
    RESET = '\x1b[39m'


def print_color(*args, color=None, **kwargs):
    """
    Print a message to the terminal in color.

    :param color: The color to print.
    """
    if color is not None:
        print(color, *args, Color.RESET, **kwargs)
    else:
        print(*args, **kwargs)
