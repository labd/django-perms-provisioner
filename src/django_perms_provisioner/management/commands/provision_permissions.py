""" manage.py command """
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from ruamel.yaml import YAML, RoundTripDumper
from ruamel import yaml
from ruamel.yaml.error import StreamMark
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

    def generate_yaml_file(self, path):
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
    def updateconfig(self, path):
        """ updateconfig file """
        permissionconfig = {}
        yaml_obj = YAML()
        with open(path, 'r') as stream:
            permissionconfig = yaml_obj.load(stream)
            self.config = permissionconfig

        print(permissionconfig)
        for group in Group.objects.all():
            if group.name not in permissionconfig.keys():
                self.create_comment(group.name)
            else:
                for perm in group.permissions.all():
                    if perm.content_type.model not in permissionconfig[group.name].keys():
                        self.create_comment(group.name, perm.content_type.model)
                        break
                    else:
                        val = "{}.{}".format(perm.content_type.app_label, perm.codename)
                        if val not in permissionconfig[group.name][perm.content_type.model]:
                            self.create_comment(group.name, perm.content_type.model, val)
        with open(path, 'w') as outfile:
            yaml.dump(permissionconfig,
                      outfile,
                      Dumper=RoundTripDumper,
                      default_flow_style=False,
                      explicit_start=True)
    def create_comment(self, groupname, modelname=None, value=None):
        """ makes a comment """
        indent = 0
        if modelname is None:
            self.make_comment("# {}:".format(groupname), indent)
            indent = 2
            group = Group.objects.get(name=groupname)
            models = {}
            for perm in group.permissions.all():
                if perm.content_type.model not in models.keys():
                    models[perm.content_type.model] = []
                models[perm.content_type.model].append("{}.{}".format(perm.content_type.app_label,
                                                                      perm.codename))
            for modelname, model in list(models.items()):
                self.make_comment("# {}:".format(modelname), indent)
                for item in model:
                    self.make_comment("# - {}".format(item), indent)
        elif value is None:
            indent = 2
            group = Group.objects.get(name=groupname)
            models = {}
            self.config.yaml_set_comment_before_after_key(groupname,
                                                          None,
                                                          None,
                                                          "{}:".format(modelname),
                                                          indent)
            for perm in group.permissions.filter(content_type__model=modelname):
                val = "- {}.{}".format(perm.content_type.app_label, perm.codename)
                self.config.yaml_set_comment_before_after_key(groupname,
                                                              None,
                                                              None,
                                                              val,
                                                              indent)
        else:
            indent = 2
            self.config[groupname].yaml_set_comment_before_after_key(modelname,
                                                                     None,
                                                                     None,
                                                                     "- {}".format(value),
                                                                     indent)
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
                            self.stdout.write("Deleted permission: {}".format(name))
                        i -= 1
                for model in permissionconfig[groupname]:
                    print(model)
                    if len(permissionconfig[groupname][model]) < 1:
                        del permissionconfig[groupname][model]
                        self.stdout.write("Deleted model: {}".format(name))

            else:
                self.stdout.write("Deleted group: {}".format(groupname))
                del permissionconfig[groupname]
        with open(path, 'w') as outfile:
            yaml.dump(permissionconfig,
                      outfile,
                      Dumper=RoundTripDumper,
                      default_flow_style=False,
                      explicit_start=True)
