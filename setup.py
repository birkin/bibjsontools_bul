# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from setuptools import find_packages, setup


install_requires = []

setup(
    name='bibjsontools',
    version='0.4',
    author='Ted Lawless',
    author_email='lawlesst@gmail.com',
    packages=find_packages(),
    package_data={'bibjsontools': ['test/data/*.*']},
    install_requires=install_requires,
)
