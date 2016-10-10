# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='smarket',
    version='1.0',
    description='Super Simple Stock Market',
    long_description=readme,
    author='Rafał Jagielski',
    author_email='bender@unit22.org',
    url='https://github.com/rjagielski/smarket',
    license=license,
    packages=find_packages(exclude=('tests',))
)
