==============================
Django Permissions Provisioner
==============================

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

.. image:: https://github.com/labd/django-perms-provisioner/workflows/Python%20Tests/badge.svg
    :target: https://github.com/labd/django-perms-provisioner/actions

.. image:: https://travis-ci.org/labd/django-perms-provisioner.svg?branch=master
    :target: https://travis-ci.org/labd/django-perms-provisioner

.. image:: http://codecov.io/github/labd/django-perms-provisioner/coverage.svg?branch=master
    :target: http://codecov.io/github/labd/django-perms-provisioner?branch=master

.. image:: https://img.shields.io/pypi/v/django-perms-provisioner.svg
    :target: https://pypi.org/project/django-perms-provisioner/


This package works like the standard Django loaddata / dumpdata commands only
it's used for creating auth.Group objects with their provided permissions.


Requirements
============

 - Python >= 3.9
 - Django >= 1.11

Installation
============

.. code-block:: shell

   pip install django_perms_provisioner


Then the only thing left before you can start using the ``Django Permissions
Provisioner`` is adding it to you installed apps.

.. code-block:: python

  INSTALLED_APPS = [
      "django_perms_provisioner",
  ]


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


.. code-block:: javascript

   {
     "groups" [{
       "name": "Group Name",
       "permissions": {
         "sites": ["site.add_site", "site.change_site"],
         "wagtailadmin": ["admin.access_admin"]
       }
     }]
   }


It is also possible to only create groups this can be done by just leaving out
the permissions.


Example:

.. code-block:: yaml

   ---
   groups:
     - name: Group Name
     - name: Next Group Name


Usage
=====

To load permissions from a configuration file

.. code-block:: shell

   ./manage.py loadperms permissions.yaml


Or to dump permissions to a configuration file

.. code-block:: shell

   ./manage.py dumpperms > permissions.yaml
