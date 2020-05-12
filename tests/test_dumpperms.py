import json
import os

import pytest
import yaml
from django.core.management import call_command

FILE_LOADER_MAPPING = {"yaml": yaml.safe_load, "json": json.load}
STR_LOADER_MAPPING = {"yaml": yaml.safe_load, "json": json.loads}


@pytest.mark.django_db
class TestDumpperms:
    @pytest.mark.parametrize("filename", ["valid.yaml", "valid.json"])
    def test_valid(self, filename, capsys):
        name, ext = os.path.splitext(filename)

        # first read the permissions to the DB
        filename = os.path.join(os.path.dirname(__file__), "files", filename)
        call_command("loadperms", filename)
        capsys.readouterr()  # Reset stdout.

        # dump and capture the permissions to stdout
        call_command("dumpperms", f"--format={ext[1:]}")
        captured = capsys.readouterr()

        loader = FILE_LOADER_MAPPING[ext[1:]]
        with open(filename, "r") as stream:
            contents = loader(stream)

        str_loader = STR_LOADER_MAPPING[ext[1:]]
        assert str_loader(captured.out) == contents, captured.out
