#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://hammer.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='hammer_variations',
    version='0.1.1',
    description='Hammering out the variations in deep learning models.',
    #long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Todd Young',
    author_email='youngmt1@ornl.gov',
    url='https://github.com/yngtodd/hammer',
    packages=[
        'hammer',
    ],
    package_dir={'hammer': 'hammer'},
    include_package_data=True,
    install_requires=[
        'toml'
    ],
    license='MIT',
    zip_safe=False,
    keywords='hammer',
    entry_points={
        'console_scripts': [
            'hammer = hammer.launch:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
