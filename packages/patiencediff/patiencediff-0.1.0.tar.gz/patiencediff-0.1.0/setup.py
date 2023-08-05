#!/usr/bin/env python3
# encoding: utf-8

from setuptools import setup, Extension

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(name="patiencediff",
      description="Python implementation of the patiencediff algorithm.",
      long_description=long_description,
      long_description_content_type='text/x-rst',
      version="0.1.0",
      maintainer="Breezy Developers",
      maintainer_email="team@breezy-vcs.org",
      license="GNU GPLv2 or later",
      url="https://www.breezy-vcs.org/",
      packages=['patiencediff'],
      test_suite='patiencediff.test_patiencediff',
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Operating System :: POSIX',
      ],
      ext_modules=[Extension('patiencediff._patiencediff_c',
          ['patiencediff/_patiencediff_c.c'])]
)
