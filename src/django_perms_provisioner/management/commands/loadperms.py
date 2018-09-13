import json
import os
from typing import Optional

import yaml
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.db import transaction

from cerberus import Validator
from django_perms_provisioner.management.schemas import PERMISSIONS_SCHEMA

FILE_CONTENT_LOADER = {"json": json.loads, "yaml": yaml.load, "yml": yaml.load}


class Command(BaseCommand):
    """Load user groups and permissions from config file.

    Permission files are relative to the location where this command is called.

    Steps:
      - Load the provided file, either json or yaml;
      - Validate file contents against the schemas.PERMISSION_SCHEMA;
      - Create or update groups with provided permissions.

    Args:
      - 1..n files to load permissions from

    """

    help = "Load user groups and permissions from config file"

    def __init__(self, *args, **kwargs):
        self.validator = Validator(PERMISSIONS_SCHEMA)
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("permission_files", nargs="+", type=str)

    @transaction.atomic()
    def handle(self, permission_files, **options):
        """Validate and process all provided files."""
        for permissions_file in permission_files:
            permissions_file = os.path.join(os.path.curdir, permissions_file)

            if not os.path.isfile(permissions_file):
                self.stderr.write(f"Permissions file ({permissions_file}) not found")
                continue

            file_contents = self.load_and_validate_file(permissions_file)
            if file_contents is not None:
                # We can safely assume the groups key is available, since the
                # contents of the file have passed the schema vaildation
                self.create_groups_with_permissions(file_contents["groups"])

        self.stdout.write(self.style.SUCCESS("Successfully loaded all permissions"))

    def load_and_validate_file(self, permissions_file) -> Optional[dict]:
        """Load and validate the file contents.

        Steps:
          - Check if there is a valid loader for the provided file (by
            extension);
          - Load the contents of the file with the appropiate loader;
          - Validate file contents against schemas.PERMISSION_SCHEMA.

        """
        filename, ext = os.path.splitext(permissions_file)

        if ext[1:] not in FILE_CONTENT_LOADER.keys():
            self.stdout.write(f"No loader found for extension: {ext}")
            return None

        loader = FILE_CONTENT_LOADER[ext[1:]]
        with open(permissions_file, "r") as stream:
            file_content = loader(stream)

        if not self.validator.validate(file_content):
            self.stderr.write(f"Permissions file ({permissions_file}) did not validate")
            self.stderr.write(self.validator.errors)
            return None

        self.stdout.write(
            f"Permissions file ({permissions_file}) validated successfully"
        )
        return file_content

    def create_groups_with_permissions(self, groups: dict):
        """Create the group and attach the provided permissions to it.

        Note: We can safely assume the required properties are in the provided
              dict since it passed validation in the previous step.

        Steps:
          - Get or create group object;
          - Add permissions (if defined) to group.

        """
        for group in groups:
            group_obj, created = Group.objects.get_or_create(name=group["name"])
            if created:
                self.stdout.write(f"Group {group['name']} created successfully.")
            else:
                self.stdout.write(f"Group {group['name']} already exists.")

            if "permissions" not in group:
                self.stdout.write(f"No permissions defined for {group['name']}")
            else:
                # Create a list with all permission objects to add to the group
                permission_list = []
                for app_label, permission_keys in group["permissions"].items():
                    permissions = self.get_permissions_for_app(
                        app_label, permission_keys
                    )
                    if permissions:
                        permission_list += permissions

                if not permission_list:
                    self.stdout.write(
                        f"No valid permissions found for {app_label}, nothing to do."
                    )
                else:
                    group_obj.permissions.set(permission_list)

    def get_permissions_for_app(self, app_label: str, permissions: list) -> list:
        """Return all valid permissions provided for app_label.

        Note: We can safely assume permissions are in the format of
              model_name.codename since they've already passed the schema
              validation.

        """
        permission_list = []
        for permission in permissions:
            model_name, codename = permission.split(".")
            try:
                permission_obj = Permission.objects.get_by_natural_key(
                    codename, app_label, model_name
                )
            except Permission.DoesNotExist:
                self.stderr.write(
                    f"Permission ({codename}, {app_label}, {model_name}) not found."
                )
                continue
            else:
                self.stdout.write(f"Adding permission ({permission_obj})")
                permission_list.append(permission_obj)
        return permission_list
