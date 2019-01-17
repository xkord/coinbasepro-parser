# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='coinbasepro',
    packages=['coinbasepro'],
    install_requires=['psycopg2', 'pika', 'cbpro', 'python-dateutil'],
    version='0.0.1',
    description='coinbasepro',
    author='Kord J.',
    author_email='xxkord@gmail.com',
    url='',
    download_url='',
    keywords=['coinbasepro', 'parse', 'requests', 'crypto'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: The MIT License (MIT)',
        'Operating System :: OS Independent'
    ],
    entry_points={
        'console_scripts': ['coinbasepro = coinbasepro:main'],
    },
    test_suite='tests',
    long_description='''
        README.md
        ------------------
    '''
)
