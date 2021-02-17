import subprocess
from pathlib import Path


class TestCli:
    def test_basic_cli(self):
        cases_dir = Path(__file__).parent / 'cases'

        case_name = 'number'
        data_filepath = cases_dir / case_name / 'data.json'
        schema_filepath = cases_dir / case_name / 'schema.json'

        command = ["jsonvl", data_filepath, schema_filepath]

        pipes = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, std_err = pipes.communicate()

        if pipes.returncode != 0:
            message = std_err.strip()
            raise Exception(message)
