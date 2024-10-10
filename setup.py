#!/usr/bin/env python
"""Defines the setup instructions for domaintools"""
import glob
import os
import sys
from os import path

from setuptools import Extension, find_packages, setup
from setuptools.command.test import test as TestCommand


MYDIR = path.abspath(os.path.dirname(__file__))
JYTHON = "java" in sys.platform
PYPY = bool(getattr(sys, "pypy_version_info", False))
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
        filenames = glob.glob(path.join(dirname, "*.py"))

        module_names = []
        for name in filenames:
            module, ext = path.splitext(path.basename(name))
            if module != "__init__":
                module_names.append(module)

        return module_names

    ext_modules = [
        Extension("domaintools." + ext, [path.join("domaintools", ext + ".py")])
        for ext in list_modules(path.join(MYDIR, "domaintools"))
    ]
    cmdclass["build_ext"] = build_ext


class PyTest(TestCommand):
    extra_kwargs = {"tests_require": ["pytest", "mock"]}

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        sys.exit(pytest.main(self.test_args))


cmdclass["test"] = PyTest

setup(
    name="domaintools_api",
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
