import json

import yaml
from django.contrib.auth.models import Group
from django.core.management import BaseCommand


def dump_data_to_yaml(data, indent=None):
    """Wrapper around yaml.safe_dump for extra args.

    To create a better (human) readable YAML format, this wrapper ensures the
    default_flow_style=False kwarg is always provided to yaml.safe_dump.

    """
    return yaml.safe_dump(data, indent=indent, default_flow_style=False)


DATA_DUMPER = {"json": json.dumps, "yaml": dump_data_to_yaml, "yml": dump_data_to_yaml}


class Command(BaseCommand):
    help = "Dump all groups and permissions to stdout"

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
        """Ouput all groups and permissions in the DB.

        Dumps all groups and permissions to stdout, this can be saved to a file
        by adding ``> filename`` this file is compatible with the ``loadperms``
        command.

        Usage:
            ./manage.py dumpperms --format=<json|yaml> --indent=2

        """
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
