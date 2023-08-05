#!/usr/bin/env python
from setuptools import setup, find_packages
import os

__doc__ = """App for Django featuring class based email sending."""


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'markdown',
]

version = '0.2.4'

setup(
    name='django-emailtools-reloaded',
    version=version,
    description=__doc__,
    long_description=read('README.rst'),
    packages=[package for package in find_packages() if package.startswith('emailtools')],
    url="https://github.com/barseghyanartur/django-emailtools-reloaded",
    author="Artur Barseghyan",
    author_email='artur.barseghyan@gmail.com',
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,
)
