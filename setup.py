#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


dependencies = [
    'docopt',
    'svgwrite',
    'svgpathtools',
    ]


packages = find_packages()


setup(
    name='svgsort',
    version='0.0.3',
    description='svg spatial sort for plotting',
    url='',
    license='MIT License',
    author='Anders Hoff',
    author_email='inconvergent@gmail.com',
    install_requires=dependencies,
    packages=packages,
    entry_points={
        'console_scripts': [
            'svgsort=svgsort:run'
            ]
        },
    zip_safe=True
    )

