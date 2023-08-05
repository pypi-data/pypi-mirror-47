#!/usr/bin/env python

from io import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='usagelogger',
    version='0.1.0',
    description='Logging usage of Python cloud apps.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/resurfaceio/logger-python',
    author='Resurface Labs',
    author_email='admin@resurface.io',
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: Log Analysis',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='logging resurface',
    packages=find_packages(exclude=['tests']),
    python_requires='>=3.4, <4',
    extras_require={
        'test': ['coverage'],
    },
    install_requires=[],
    project_urls={
        'Bug Reports': 'https://github.com/resurfaceio/logger-python/issues',
        'Source': 'https://github.com/resurfaceio/logger-python'
    }
)
