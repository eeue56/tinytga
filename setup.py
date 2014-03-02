#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

try:
    license = open('LICENSE').read()
except:
    license = None

try:
    readme = open('README.md').read()
except:
    readme = None

setup(name='tinytga',
      version='1.0.0',
      description='Tiny TGA loader without need for 3rd party libraries',
      long_description=readme,
      license=license,
      url='http://github.com/eeue56/tinytga/',
      author='Enalicho',
      author_email='enalicho@gmail.com',
      packages=find_packages(),
      requires=[],
)
