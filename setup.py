from setuptools import find_packages, setup


tests_require = [
    "coverage",
    "pytest==9.0.3",
    "pytest-cov==3.0.0",
    "pytest-django==4.5.2",
    # Linting
    "ruff",
]

setup(
    name="django-perms-provisioner",
    version="0.0.6",
    description="Provision django instances with usergroups and permissions",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/labd/django-perms-provisioner",
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    python_requires=">=3.11",
    install_requires=["Cerberus>=1.3.2,<2", "Django>=3.2", "PyYAML>=5.3.1,<7"],
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
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.2",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    zip_safe=False,
)
