""" manage.py command """
from django.core.management import BaseCommand
from django_perms_provisioner.generate_file import generate_yaml_file
from django_perms_provisioner.cleanup import cleanup
from django_perms_provisioner.updateconfig import updateconfig


class Command(BaseCommand):
    """ Generate yaml file from groups and permissions """
    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)
        parser.add_argument(
            '--updateconfig',
            action='store_true',
            dest='updateconfig',
            default=False,
            help='add a comment every permission and group that not exists in config file',
        )
        parser.add_argument(
            '-u',
            action='store_true',
            dest='updateconfig',
            default=False,
            help='add a comment every permission and group that not exists in config file',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='cleanup',
            default=False,
            help='Removes unused permissions and groups from config file',
        )
        parser.add_argument(
            '-c',
            action='store_true',
            dest='cleanup',
            default=False,
            help='Removes unused permissions and groups from config file',
        )

    def handle(self, *args, **options):
        path = options["filename"][0]
        if options['updateconfig']:
            updateconfig(path)
        elif options['cleanup']:
            cleanup(path)
        else:
            generate_yaml_file(path)
