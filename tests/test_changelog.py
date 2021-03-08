import re
from pathlib import Path

CHANGELOG_FILEPATH = Path(__file__).parent.parent / 'CHANGELOG.rst'


class TestChangelog:
    def test_changelog(self):
        with open(CHANGELOG_FILEPATH, 'r') as f:
            lines = f.readlines()
            self.check_version_line(lines, 0)

    def check_version_line(self, lines, i):
        assert re.match(r'^v[0-9]+\.[0-9]+\.[0-9]+\n$', lines[i]), f"Version is invalid: {lines[i]}"
        self.check_sep_line(lines, i + 1)

    def check_sep_line(self, lines, i):
        assert re.match(r'^[-]+$', lines[i]), "Separator expected after version line"
        length = len(lines[i - 1])
        assert len(lines[i]) == length, f"Separator expected to have {length} dashes based on version {lines[i - 1]}"
        self.check_blank_line(lines, i + 1)

    def check_blank_line(self, lines, i):
        assert lines[i] == '\n', "Expected a blank line"

        if lines[i + 1].startswith('v'):
            self.check_version_line(lines, i + 1)
        elif lines[i + 1].startswith('*'):
            assert lines[i - 1].startswith('-'), "Expected a separator before a blank space before a change."
            self.check_change_line(lines, i + 1)
        else:
            raise ValueError(f"Expected a change or a version after a blank line at {i}")

    def check_change_line(self, lines, i):
        assert re.match(r'^\*\s', lines[i]), "Invalid change line format"

        if i == len(lines) - 1:
            return
        elif lines[i + 1].startswith('*'):
            self.check_change_line(lines, i + 1)
        elif lines[i + 1] == '\n':
            self.check_blank_line(lines, i + 1)
        else:
            raise ValueError(f"Invalid CHANGELOG on line {i + 1}: {lines[i + 1]}")
