#!/usr/bin/env python
"""
This is a shim to allow installation and releases with older tools that expect setup.py.
The actual configuration is in pyproject.toml.
"""

from setuptools import setup

if __name__ == "__main__":
    setup()
