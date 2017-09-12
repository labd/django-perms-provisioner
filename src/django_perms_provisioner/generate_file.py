""" Generate yaml file """
from django.contrib.auth.models import Group
from ruamel import yaml


def generate_yaml_file(path):
    """ Generate the yaml file """
    permissions = {}
    for group in Group.objects.all():
        permissions[group.name] = {}
        for permission in group.permissions.all():
            if permission.content_type.model not in permissions[group.name].keys():
                permissions[group.name][permission.content_type.model] = []
            val = "{}.{}".format(permission.content_type.app_label, permission.codename)
            permissions[group.name][permission.content_type.model].append(val)
    yaml_file = open(path, 'w')
    yaml.dump(permissions, yaml_file, default_flow_style=False, explicit_start=True)
    yaml_file.close()
