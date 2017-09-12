""" Cleans up config file """

import sys
from django.contrib.auth.models import Group
from ruamel.yaml import YAML, RoundTripDumper
from ruamel import yaml


def cleanup(path):
    """ removes unused permissions and groups from config file """
    permissionconfig = {}
    yaml_obj = YAML()
    with open(path, 'r') as stream:
        permissionconfig = yaml_obj.load(stream)
    for groupname, group in list(permissionconfig.items()):
        if Group.objects.filter(name=groupname).count() >= 1:
            for model, perms in list(group.items()):
                i = len(perms) - 1
                while i >= 0:
                    perm = perms[i]
                    app_label, name = perm.rsplit('.', 1)
                    if not Group.objects.filter(name=groupname,
                                                permissions__codename=name,
                                                permissions__content_type__app_label=app_label,
                                                permissions__content_type__model=model).exists():
                        del permissionconfig[groupname][model][i]
                        sys.stdout.write("Deleted permission: {}".format(name))
                    i -= 1
            for model in permissionconfig[groupname]:
                if len(permissionconfig[groupname][model]) < 1:
                    del permissionconfig[groupname][model]
                    sys.stdout.write("Deleted model: {}".format(name))

        else:
            sys.stdout.write("Deleted group: {}".format(groupname))
            del permissionconfig[groupname]
    with open(path, 'w') as outfile:
        yaml.dump(permissionconfig,
                  outfile,
                  Dumper=RoundTripDumper,
                  default_flow_style=False,
                  explicit_start=True)
