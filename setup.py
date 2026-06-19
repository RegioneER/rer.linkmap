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
    setup(
        classifiers=[
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
        ],
        python_requires=">=3.10,<3.14",
    )
