#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__version__ = '0.1.0'
__author__  = 'Zeuxis Lo'
__email__   = 'seekstudio@gmail.com'

setup(
    name='pluginplot',
    author=__author__,
    author_email=__email__,
    version=__version__,
    license='BSD',
    url='https://github.com/zeuxisoo/python-pluginplot',
    description='Yet another simple plugin system for Python like WordPress plugin system',
    install_requires=[],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
)
