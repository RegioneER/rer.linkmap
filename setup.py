#!/usr/bin/env python
"""
This is a shim to allow installation and releases with older tools that expect setup.py.
The actual configuration is in pyproject.toml.
"""

try:
    from setuptools import setup
except ImportError:

    def setup(**kwargs):
        pass


if __name__ == "__main__":
    setup()
