""" manage.py command """
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.error import CommentMark, StreamMark
from ruamel.yaml.tokens import CommentToken


class Command(BaseCommand):
    """ Generate yaml file from groups and permissions """
    yaml = None
    pre_comments = []
    config = None
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
            self.updateconfig(path)
        elif options['cleanup']:
            self.cleanup(path)
        else:
            self.generate_yaml_file(path)

    def generate_yaml_file(self,path):
        """ Generate the yaml file """
        yaml_file = open(path, 'w')
        yaml_file.write("---")
        yaml_file.write('\n')
        for group in Group.objects.all():
            yaml_file.write(group.name + ":\n")
            for permission in group.permissions.all():
                yaml_file.write('  "{}.{}": "{}"\n'.format(permission.content_type.app_label,
                                                           permission.codename,
                                                           permission.content_type.model))
        yaml_file.close()

    def updateconfig(self, path):
        """ updateconfig file """
        permissionconfig = {}
        self.yaml = YAML()
        yaml = self.yaml
        with open(path, 'r') as stream:
            permissionconfig = yaml.load(stream)
            self.config = permissionconfig
        for group in Group.objects.all():
            if group.name not in permissionconfig.keys():
                self.create_comment(group.name)
            else:
                for permission in group.permissions.all():
                    key = "{}.{}".format(permission.content_type.app_label, permission.codename)
                    value = permission.content_type.model
                    if (key not in permissionconfig[group.name].keys()
                            or permissionconfig[group.name][key] != value):
                        self.create_comment(group.name, permission.codename,
                                           permission.content_type.app_label,
                                           permission.content_type.model)
        with open(path, 'w') as outfile:
            yaml.dump(permissionconfig, outfile)

    def create_comment(self, groupname, permissionname=None, app_label=None, model=None):
        """ makes a comment """
        value = "{}.{}: {}".format(app_label, permissionname, model)
        indent = 0

        if permissionname != None:
            indent = 2
            self.config.yaml_set_comment_before_after_key(groupname, None, None, value, indent)
        else:
            value = "# {}:".format(groupname)
            group = Group.objects.get(name=groupname)
            self.make_comment(value, 0)
            for permission in group.permissions.all():
                value = "# {}.{}: {}\n".format(permission.content_type.app_label,
                                               permission.codename,
                                               permission.content_type.model)
                self.make_comment(value, 2)

    def make_comment(self, value, indent):
        """ Creates a comment at the top of the file """
        start_mark = StreamMark(None, 5, 2, indent)   # column 0
        commenttoken = CommentToken(value, start_mark, None)
        if self.config.ca.comment is None:
            self.config.ca.comment = [None, self.pre_comments]
        else:
            self.pre_comments = self.config.ca.comment[1]
        self.pre_comments.append(commenttoken)

    def cleanup(self, path):
        """ checks if group or permission exists in the database otherwise it deletes it from the config file """
        yaml = YAML()
        permissionconfig = {}
        with open(path, 'r') as stream:
            permissionconfig = yaml.load(stream)
        for groupname, group in list(permissionconfig.items()):
            if Group.objects.filter(name=groupname).count() >= 1:
                for perm, model in list(group.items()):
                    app_label, name = perm.rsplit('.', 1)
                    if not Group.objects.filter(name= groupname,
                                                permissions__codename=name,
                                                permissions__content_type__app_label=app_label,
                                                permissions__content_type__model=model).exists():
                        del permissionconfig[groupname][perm]
                        self.stdout.write("Deleted permission: {}".format(name))
            else:
                self.stdout.write("Deleted group: {}".format(groupname))
                del permissionconfig[groupname]
        with open(path, 'w') as outfile:
            yaml.dump(permissionconfig, outfile)