from setuptools import find_packages, setup

docs_require = ["sphinx>=1.4.0"]

tests_require = [
    "coverage",
    "pytest==3.8.1",
    "pytest-cov==2.6.0",
    "pytest-django==3.4.3",
    # Linting
    "isort==4.2.5",
    "flake8==3.5.0",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==3.1.0",
]

setup(
    name="django-perms-provisioner",
    version="0.0.3",
    description="Provision django instances with usergroups and permissions",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/labd/django-perms-provisioner",
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    install_requires=["Cerberus>=1.3.2,<2", "Django>=1.11", "PyYAML>=5.3.1,<6"],
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    use_scm_version=True,
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    zip_safe=False,
)
