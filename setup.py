#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from setuptools import find_namespace_packages, setup

setup(
    name='Langevin_LLPS',
    version='0.1.0',
    license='MIT',
    description='toy model for simulating mechanical constraint LLPS',
    author='Chen Lin',
    author_email='linchen4869@ucla.edu',
    url='',
    packages=find_namespace_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'': ['*.yaml']},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.8',
    install_requires=[
        'hydra-core==1.3.1',
        'matplotlib',
    ],
)