#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='django-switch-templatetag',

    url="https://chris-lamb.co.uk/projects/django-switch-templatetag",
    version='1.0.0',
    description="Simple switch tag for Django templates.",

    author="Chris Lamb",
    author_email="chris@chris-lamb.co.uk",
    license="BSD",

    packages=find_packages(),
    include_package_data=True,
)
