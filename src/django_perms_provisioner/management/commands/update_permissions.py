""" manage.py command """
from django.contrib.auth.models import Group, ContentType, Permission
from django.core.management import BaseCommand
from ruamel.yaml import YAML


class Command(BaseCommand):
    """ update the database based on the config file """
    yaml = None

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['filename'][0]
        yaml_obj = YAML()
        permissionconfig = {}
        with open(path, 'r') as stream:
            permissionconfig = yaml_obj.load(stream)
        for gname, models in list(permissionconfig.items()):
            group, group_created = Group.objects.get_or_create(name=gname)
            if group_created:
                print("Created group: {}".format(gname))
            for modelname, permissions in list(models.items()):
                for perm in permissions:
                    applabel, name = perm.rsplit('.', 1)
                    ct = ContentType.objects.get(app_label=applabel, model=modelname)
                    if not Group.objects.filter(name=gname,
                                                permissions__codename=name,
                                                permissions__content_type=ct).exists():
                        new_perm, perm_created = Permission.objects.get_or_create(content_type=ct,
                                                                                  codename=name)
                        if perm_created:
                            print("Created permission: {} and added to group: {}".format(name,
                                                                                         gname))
                        else:
                            print("Permission: {} added to group: {}".format(name, gname))
                        group.permissions.add(new_perm)
        for group in Group.objects.all():
            if group.name not in permissionconfig.keys():
                print("Deleted group: {}".format(group.name))
                Group.objects.filter(id=group.id).delete()
            else:
                for perm in group.permissions.all():
                    val = "{}.{}".format(perm.content_type.app_label, perm.codename)
                    if (perm.content_type.model not in permissionconfig[group.name].keys() or
                            val not in permissionconfig[group.name][perm.content_type.model]):
                        print("Deleted permission: {} from group: {}".format(perm.codename,
                                                                             group.name))
                        group.permissions.remove(perm)
