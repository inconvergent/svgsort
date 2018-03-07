#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


dependencies = [
    'docopt',
    'svgwrite',
    'svgpathtools==1.3.3',
    ]


packages = find_packages()


setup(
    name='svgsort',
    version='1.0.0',
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
    dependency_links=['git+https://github.com/inconvergent/svgpathtools.git@master#egg=svgpathtools-1.3.3'],
    zip_safe=True
    )

