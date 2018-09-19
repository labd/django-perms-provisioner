import json
from collections import defaultdict

import yaml
from django.contrib.auth.models import Group
from django.core.management import BaseCommand


def dump_data_to_yaml(data, indent=None):
    return yaml.safe_dump(data, indent=indent, default_flow_style=False)


DATA_DUMPER = {"json": json.dumps, "yaml": dump_data_to_yaml, "yml": dump_data_to_yaml}


class Command(BaseCommand):
    """Dump groups and permissions data to stdout."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--format",
            default="yaml",
            help="Specifies the output serialization format for permissions.",
        )
        parser.add_argument(
            "--indent",
            type=int,
            default=2,
            help="Specifies the indent level to use when pretty-printing output.",
        )

    def handle(self, **options):
        format = options["format"]
        indent = options["indent"]

        if format not in DATA_DUMPER.keys():
            available_formats = ", ".join(DATA_DUMPER.keys())
            self.stderr.write(
                self.style.ERROR(
                    f"Provided format is not valid, use one of: {available_formats}"
                )
            )
            return

        groups_permissions_data = []
        for group in Group.objects.all():
            group_data = {"name": group.name}

            if group.permissions.exists():
                group_data["permissions"] = {}
                for permission in group.permissions.all():
                    codename, app_label, model_name = permission.natural_key()

                    if app_label not in group_data["permissions"]:
                        group_data["permissions"][app_label] = []

                    group_data["permissions"][app_label].append(
                        f"{model_name}.{codename}"
                    )

            groups_permissions_data.append(group_data)

        dumper = DATA_DUMPER[format]
        self.stdout.write(dumper({"groups": groups_permissions_data}, indent=indent))
