#!/usr/bin/env python
from setuptools import setup


setup(
    name='ip_assembler',
    description='Banned IP processing for .htaccess locations like Wordpress.',
    version='0.0.1',
    author='Alexander Herrmann',
    author_email='darignac@gmail.com',
    license='MIT',
    url='https://github.com/dArignac/ip_assembler',
    packages=['ip_assembler'],
    long_description=open('README.rst').read(),
    install_requires=[
        'Django>=1.6,<1.7',
        'django-shared',
    ],
    dependency_links=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ]
)
