import json
from pathlib import Path

import pytest
import yaml
from django.core.management import call_command

FILE_LOADER_MAPPING = {"yaml": yaml.safe_load, "json": json.load}
STR_LOADER_MAPPING = {"yaml": yaml.safe_load, "json": json.loads}


@pytest.mark.django_db
class TestDumpperms:
    @pytest.mark.parametrize("input_file, expected_file", [
        ("valid.yaml", "valid.yaml"),
        ("valid.json", "valid.json"),
    ])
    def test_valid(self, input_file, expected_file, capsys):
        input_file = Path(__file__).parent / "files" / input_file
        expected_file = Path(__file__).parent / "files" / expected_file

        # first read the permissions to the DB
        call_command("loadperms", input_file)
        capsys.readouterr()  # Reset stdout.

        # dump and capture the permissions to stdout and read them back
        call_command("dumpperms", f"--format={expected_file.suffix[1:]}")
        captured = capsys.readouterr()

        loader = FILE_LOADER_MAPPING[expected_file.suffix[1:]]
        with expected_file.open("r") as stream:
            expected_contents = loader(stream)

        str_loader = STR_LOADER_MAPPING[expected_file.suffix[1:]]
        assert str_loader(captured.out) == expected_contents, captured.out
