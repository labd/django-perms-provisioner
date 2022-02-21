from django.conf import settings


def pytest_configure():
    settings.configure(
        MIDDLEWARE_CLASSES=[],
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "django_perms_provisioner",
        ],
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "unique-snowflake",
            }
        },
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite"}
        },
        SECRET_KEY="test",
    )
