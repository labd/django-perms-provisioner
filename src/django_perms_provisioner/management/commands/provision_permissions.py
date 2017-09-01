from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand


class Command(BaseCommand):
    """ command """

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)

    def handle(self, *args, **options):
        """ s """
        yaml_file = open(options['file_name'][0], 'w')
        
        yaml_file.close()