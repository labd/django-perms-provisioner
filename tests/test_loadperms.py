import os

import pytest
from django.contrib.auth import models
from django.core.management import call_command


@pytest.mark.django_db
class TestLoadperms:
    @pytest.mark.parametrize("filename", ["valid.yaml", "valid.json"])
    def test_valid(self, filename):
        yaml_file = os.path.join(os.path.dirname(__file__), "files", filename)
        call_command("loadperms", yaml_file)

        group_admin = models.Group.objects.filter(name="Group Admin").first()
        user_admin = models.Group.objects.filter(name="User Admin").first()
        only_group = models.Group.objects.filter(name="Only Group").first()

        assert group_admin and user_admin and only_group

        assert group_admin.permissions.count() == 3
        for permission in group_admin.permissions.all():
            perm, app, model = permission.natural_key()
            assert app == "auth"
            assert model == "group"
            assert perm in ("add_group", "change_group", "delete_group")

        assert user_admin.permissions.count() == 3
        for permission in user_admin.permissions.all():
            perm, app, model = permission.natural_key()
            assert app == "auth"
            assert model == "user"
            assert perm in ("add_user", "change_user", "delete_user")

        assert only_group.permissions.count() == 0
