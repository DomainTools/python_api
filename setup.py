#!/usr/bin/env python
"""Defines the setup instructions for domaintools"""
import glob
import os
import subprocess
import sys
from os import path

from setuptools import Extension, find_packages, setup
from setuptools.command.test import test as TestCommand

requires = ['requests']
packages = ['domaintools']
if sys.version_info[0] >= 3 and sys.version_info[1] >= 5:
    packages.append('domaintools_async')
    requires.append('aiohttp==2.3.6')
elif sys.version_info[0] == 2 and sys.version_info[1] <= 6:
    requires.extend(['ordereddict', 'argparse'])

MYDIR = path.abspath(os.path.dirname(__file__))
JYTHON = 'java' in sys.platform
PYPY = bool(getattr(sys, 'pypy_version_info', False))
CYTHON = False
if not PYPY and not JYTHON:
    try:
        from Cython.Distutils import build_ext
        CYTHON = True
    except ImportError:
        pass

cmdclass = {}
ext_modules = []
if CYTHON:
    def list_modules(dirname):
        filenames = glob.glob(path.join(dirname, '*.py'))

        module_names = []
        for name in filenames:
            module, ext = path.splitext(path.basename(name))
            if module != '__init__':
                module_names.append(module)

        return module_names

    ext_modules = [
        Extension('domaintools.' + ext, [path.join('domaintools', ext + '.py')])
        for ext in list_modules(path.join(MYDIR, 'domaintools'))]
    cmdclass['build_ext'] = build_ext


class PyTest(TestCommand):
    extra_kwargs = {'tests_require': ['pytest', 'mock']}

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


cmdclass['test'] = PyTest

try:
   import pypandoc
   readme = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError, RuntimeError):
   readme = ''

setup(name='domaintools_api',
      version='0.2.3',
      description="DomainTools' Official Python API",
      long_description=readme,
      author='DomainTools',
      author_email='timothy@domaintools.com',
      url='https://github.com/domaintools/python_api',
      license="MIT",
      entry_points={
        'console_scripts': [
            'domaintools = domaintools.cli:run',
        ]
      },
      packages=packages,
      requires=[package.split('==')[0] for package in requires],
      install_requires=requires,
      cmdclass=cmdclass,
      ext_modules=ext_modules,
      keywords='Python, Python3',
      classifiers=['Development Status :: 6 - Mature',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Utilities'],
      **PyTest.extra_kwargs)
