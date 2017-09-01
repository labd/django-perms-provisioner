from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand


class Command(BaseCommand):
    """ Generate yaml file from groups and permissions"""

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        """ Generate the yaml file """
        yaml_file = open(options['file_name'][0], 'w')
        yaml_file.write("---")
        yaml_file.write('\n')
        for group in Group.objects.all():
            yaml_file.write(group.name + ":\n")
            for permission in group.permissions.all():
                yaml_file.write('  "')
                yaml_file.write(permission.content_type.app_label)
                yaml_file.write('.')
                yaml_file.write(permission.codename)
                yaml_file.write('": ')
                yaml_file.write('"')
                yaml_file.write(permission.content_type.model)
                yaml_file.write('"\n')
        yaml_file.close()
