#!/usr/bin/env python3
"""wirelesstagpy setup script."""

from __future__ import print_function
import io

from setuptools import setup, find_packages

import wirelesstagpy.constants as CONST

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

PACKAGES = find_packages(exclude=['test', 'test.*', 'test*'])

setup(
    name='wirelesstagpy',
    version=CONST.__version__,
    url='https://github.com/sergeymaysak/wirelesstagpy/',
    license='MIT',
    author='Sergiy Maysak',
    tests_require=['pytest'],
    install_requires=['requests>=2.18.4'],
    author_email='sergey.maysak@gmail.com',
    description='Simple python wrapper over wirelesstags REST API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=PACKAGES,
    python_requires='>=3',
    py_modules=['wirelesstagpy'],
    include_package_data=True,
    platforms='any',
    test_suite='test',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Home Automation'
        ],
    extras_require={
        'testing': ['unittest'],
    }
)
