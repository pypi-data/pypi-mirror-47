#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'boto3>=1.9.0', 'pandas>=0.20.0', 'kubernetes>=9.0.0']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'boto3>=1.9.0', 'pandas>=0.20.0', 'kubernetes>=9.0.0']

setup(
    author="Konstantin Taletskiy",
    author_email='konstantin@taletskiy.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="CLI to schedule Jupyter Notebook execution with Papermill and Argo",
    entry_points={
        'console_scripts': [
            'yason=yason.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='yason',
    name='yason',
    packages=find_packages(include=['yason']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ktaletsk/yason',
    version='0.1.1',
    zip_safe=False,
)
