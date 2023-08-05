#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt', 'r') as reqs:
    requirements = reqs.read().split('\n')

test_requirements = ['pytest', ]

setup(
    author="John Hardy",
    author_email='john@johnchardy.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Utilities to manage ec2 instances and asg's",
    entry_points={
        'console_scripts': [
            'ec2ools=ec2ools.cli:main',
            'ec2ools-eip=ec2ools.cli_eip:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='ec2ools',
    name='ec2ools',
    packages=find_packages(include=['ec2ools']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ibejohn818/ec2ools',
    version='0.1.2',
    zip_safe=False,
)
