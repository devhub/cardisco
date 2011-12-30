#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(name='cardisco',
      version='1.0',
      description='HTML Autodiscovery Library',
      author='Mark Lee',
      packages=find_packages(),
      install_requires=[
          'html5lib',
          'httplib2',
          'importlib',
      ])
