"""Configuration for test environment"""
import sys

collect_ignore = []

if sys.version_info < (3, 5):
    collect_ignore.append("test_async.py")
