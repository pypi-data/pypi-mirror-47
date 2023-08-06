#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

VERSION = "v0.4.0"
PACKAGE_NAME = "lcr-api"
HERE = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_URL = "https://github.com/philipbl/LCR-API/archive/" "{}.zip".format(VERSION)

PACKAGES = find_packages(exclude=["tests", "tests.*"])

REQUIRES = ["requests>=2,<3"]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license="MIT License",
    download_url=DOWNLOAD_URL,
    author="Philip Lundrigan",
    author_email="philiplundrigan@gmail.com",
    description="An API for The Church of Jesus Christ of Latter-day Saint's Leader and Clerk Resources (LCR)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/philipbl/LCR-API",
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    install_requires=REQUIRES,
    test_suite="tests",
)
