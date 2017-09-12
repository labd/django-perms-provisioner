""" Update the config file """
from django.contrib.auth.models import Group
from ruamel.yaml import YAML, RoundTripDumper
from ruamel import yaml
from ruamel.yaml.error import StreamMark
from ruamel.yaml.tokens import CommentToken


def updateconfig(path):
    """ add not existing permissions or groups to config file as comments """
    permissionconfig = {}
    yaml_obj = YAML()
    config = None
    def create_comment(groupname, modelname=None, value=None):
        """ makes a comment """
        indent = 0
        if modelname is None:
            make_comment("# {}:".format(groupname), indent)
            indent = 2
            group = Group.objects.get(name=groupname)
            models = {}
            for perm in group.permissions.all():
                if perm.content_type.model not in models.keys():
                    models[perm.content_type.model] = []
                models[perm.content_type.model].append("{}.{}".format(perm.content_type.app_label,
                                                                      perm.codename))
            for modelname, model in list(models.items()):
                make_comment("# {}:".format(modelname), indent)
                for item in model:
                    make_comment("# - {}".format(item), indent)
        elif value is None:
            indent = 2
            group = Group.objects.get(name=groupname)
            models = {}
            config.yaml_set_comment_before_after_key(groupname,
                                                     None,
                                                     None,
                                                     "{}:".format(modelname),
                                                     indent)
            for perm in group.permissions.filter(content_type__model=modelname):
                val = "- {}.{}".format(perm.content_type.app_label, perm.codename)
                config.yaml_set_comment_before_after_key(groupname,
                                                         None,
                                                         None,
                                                         val,
                                                         indent)
        else:
            indent = 2
            config[groupname].yaml_set_comment_before_after_key(modelname,
                                                                None,
                                                                None,
                                                                "- {}".format(value),
                                                                indent)
    def make_comment(value, indent):
        """ Creates a comment at the top of the file """
        pre_comments = []
        start_mark = StreamMark(None, 5, 2, indent)   # column 0
        commenttoken = CommentToken(value, start_mark, None)
        if config.ca.comment is None:
            config.ca.comment = [None, pre_comments]
        else:
            pre_comments = config.ca.comment[1]
        pre_comments.append(commenttoken)


    with open(path, 'r') as stream:
        permissionconfig = yaml_obj.load(stream)
        config = permissionconfig
    for group in Group.objects.all():
        if group.name not in permissionconfig.keys():
            create_comment(group.name)
        else:
            for perm in group.permissions.all():
                if perm.content_type.model not in permissionconfig[group.name].keys():
                    create_comment(group.name, perm.content_type.model)
                    break
                else:
                    val = "{}.{}".format(perm.content_type.app_label, perm.codename)
                    if val not in permissionconfig[group.name][perm.content_type.model]:
                        create_comment(group.name, perm.content_type.model, val)
    with open(path, 'w') as outfile:
        yaml.dump(permissionconfig,
                  outfile,
                  Dumper=RoundTripDumper,
                  default_flow_style=False,
                  explicit_start=True)
