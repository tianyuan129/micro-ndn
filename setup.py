#!/usr/bin/env python3
from gettext import find
from setuptools import setup, find_packages
setup(
    name='micro-ndn',
    description='A Docker-based NDN Emulation Tool',
    url='https://github.com/tianyuan129/micro-ndn',
    author='Tianyuan Yu',
    author_email='tianyuan@cs.ucla.edu',
    license='Apache License 2.0',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: System :: Networking',

        'License :: OSI Approved :: Apache License 2.0',

        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='NDN',
    packages=['microndn'],
    install_requires=[
        "python-ndn >= 0.3.post2",
        "PyYAML >= 6.0",
        "cryptography>=2.8",
        "docker>=6.0.0",
    ],
    python_requires=">=3.9",
)
