import subprocess

import pytest


class TestCli:
    @pytest.fixture
    def example_files(self, tmp_path):
        tmp_dir = tmp_path / 'example'
        tmp_dir.mkdir()
        return tmp_dir / 'data.json', tmp_dir / 'schema.json'

    def test_cli(self, example_files):
        data_file, schema_file = example_files
        data_file.write_text("\"hello\"")
        schema_file.write_text("\"string\"")

        command = ["jsonvl", data_file, schema_file]
        pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, std_err = pipes.communicate()

        if pipes.returncode != 0:
            message = std_err.strip()
            raise Exception(message)

    def test_cli_fail(self, example_files):
        data_file, schema_file = example_files
        data_file.write_text("\"hello\"")
        schema_file.write_text("\"number\"")

        command = ["jsonvl", data_file, schema_file]
        pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, std_err = pipes.communicate()

        if pipes.returncode != 0:
            message = str(std_err.strip())
            expected = "Value hello is not of expected type number"
            assert expected in message
