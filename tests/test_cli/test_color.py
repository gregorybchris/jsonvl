import builtins

import pytest

from jsonvl._cli.color import Color, print_color


class TestErrorMessages:
    @pytest.fixture(params=[
        Color.BLUE,
        Color.CYAN,
        Color.GREEN,
        Color.ORANGE,
        Color.RED,
    ])
    def color_value(self, request):
        return request.param

    def test_print_color(self, color_value, monkeypatch):
        test_message = 'test_message'

        def mock_print(color, message, reset, *args, **kwargs):
            assert color == color_value
            assert message == test_message
            assert reset == Color.RESET

        monkeypatch.setattr(builtins, "print", mock_print)

        print_color(test_message, color=color_value)

    def test_print_no_color(self, monkeypatch):
        test_message = 'test_message'

        def mock_print(message, *args, **kwargs):
            assert message == test_message

        monkeypatch.setattr(builtins, "print", mock_print)

        print_color(test_message)
