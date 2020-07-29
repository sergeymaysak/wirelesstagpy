#!/usr/bin/env python3
"""wirelesstagpy setup script."""

from __future__ import print_function
import io

from setuptools import setup, find_packages

import wirelesstagpy.constants as CONST

def read(*filenames, **kwargs):
    """Join multiple files."""
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as file:
            buf.append(file.read())
    return sep.join(buf)

LONG_DESCRIPTION = read('README.md', 'CHANGES.md', 'TODO.md')
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
    long_description=LONG_DESCRIPTION,
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
