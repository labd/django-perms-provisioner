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
    ---
    # admin:
        # logentry:
        # - admin.add_logentry
        # - admin.change_logentry
        # - admin.delete_logentry
    test:
        # contenttype:
        # - contenttypes.add_contenttype
        # - contenttypes.change_contenttype
        # - contenttypes.delete_contenttype
        group:
        - auth.change_group
        - auth.delete_group
        logentry:
        - admin.add_logentry
        - admin.change_logentry
        - admin.delete_logentry
        permission:
        - auth.add_permission
        - auth.change_permission
        - auth.delete_permission
        rule:
        - robots.add_rule
        - robots.change_rule
        - robots.delete_rule
        session:
        - sessions.add_session
        - sessions.change_session
        - sessions.delete_session
        site:
        - sites.add_site
        - sites.change_site
        - sites.delete_site
        url:
        - robots.add_url
        - robots.change_url
        - robots.delete_url
        user:
        - user.add_user
        - user.change_user
        - user.delete_user
```