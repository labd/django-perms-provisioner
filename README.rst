===================
django_perms_provisioner
===================


Installation
============

.. code-block:: shell

   pip install django_perms_provisioner


Example config

=============
```yaml
    test:
        # admin.add_logentry: logentry
        # admin.change_logentry: logentry
        # admin.delete_logentry: logentry
        auth.add_group: group
        auth.change_group: group
        auth.delete_group: group
        auth.add_permission: permission
        auth.change_permission: permission
        auth.delete_permission: permission
        contenttypes.add_contenttype: contenttype
        contenttypes.change_contenttype: contenttype
        contenttypes.delete_contenttype: contenttype
        robots.add_rule: rule
        robots.change_rule: rule
        robots.delete_rule: rule
        robots.add_url: url
        robots.change_url: url
        robots.delete_url: url
        sessions.add_session: session
        sessions.change_session: session
        sessions.delete_session: session
        sites.add_site: site
        sites.change_site: site
        sites.delete_site: site
        user.add_user: user
        user.change_user: user
        user.delete_user: user
    admin:
        # admin.add_logentry: logentry
        # admin.change_logentry: logentry
        # admin.delete_logentry: logentry
    {}
```