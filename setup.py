#!/usr/bin/env python
from setuptools import setup


setup(
    name='ip_assembler',
    description='TODO',
    version='0.0.1',
    author='Alexander Herrmann',
    author_email='darignac@gmail.com',
    license='MIT',
    url='https://github.com/dArignac/ip_assembler',
    packages=['ip_assembler'],
    # long_description=open('README.md').read(),
    install_requires=[
        'Django>=1.6,<1.7',
    ],
    dependency_links=[
    ]
)
