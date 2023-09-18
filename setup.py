from setuptools import find_packages, setup


tests_require = [
    "coverage",
    "pytest==7.4.2",
    "pytest-cov==4.1.0",
    "pytest-django==4.5.2",
    # Linting
    "isort==5.12.0",
    "flake8==5.0.4",
    "flake8-blind-except==0.2.1",
    "flake8-debugger==4.1.2",
]

setup(
    name="django-perms-provisioner",
    version="0.0.8",
    description="Provision django instances with usergroups and permissions",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/labd/django-perms-provisioner",
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    install_requires=["Cerberus>=1.3.5,<2", "Django>=4.0", "PyYAML>=5.3.1,<7"],
    tests_require=tests_require,
    extras_require={"test": tests_require},
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    zip_safe=False,
)
