#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


setup(name='svgsort',
      version='3.0.0',
      description='svg spatial sort for plotting',
      url='https://github.com/inconvergent/svgsort',
      license='MIT License',
      author='Anders Hoff',
      author_email='inconvergent@gmail.com',
      install_requires=['docopt', 'svgwrite', 'numpy', 'scipy'],
      packages=find_packages(),
      entry_points={'console_scripts': ['svgsort=svgsort:main']},
      zip_safe=True
      )

