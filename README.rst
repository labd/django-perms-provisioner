==============================
Django Permissions Provisioner
==============================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black


This package works like the standard Django loaddata / dumpdata commands only
it's used for creating auth.Group objects with their provided permissions.


Installation
============

.. code-block:: shell

   pip install django_perms_provisioner


Usage
=====

To load permissions from a configuration file

.. code-block:: shell

   ./manage.py loadperms permissions.yaml


Or to dump permissions to a configuration file

.. code-block:: shell

   ./manage.py dumpperms > permissions.yaml


Configuration
=============

Configuration can either be done via providing a ``YAML`` or ``JSON`` file. Your
file needs to have one of the following extensions: .json, .yaml, .yml, and
their approriate contents of course.

Examples:

.. code-block:: yaml

   ---
   groups:
     - name: Group Name
       permissions:
         sites:
            - site.add_site
            - site.change_site
          wagtailadmin:
            - admin.access_admin


.. code-block:: json

   {
     "groups" [
       {
         "name": "Group Name",
         "permissions": {
           "sites": ["site.add_site", "site.change_site"],
           "wagtailadmin": ["admin.access_admin"]
         }
       }
     ]
   }


It is also possible to only create a group this can be done by leaving out the
permissions object (dict).
