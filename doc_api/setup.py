#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="docapi",
    version="1.0",
    description="Python document semantic storage",
    author="Martin Miksanik",
    author_email="martin@miksanik.net",
    url="https://www.python.org",
    packages=find_packages(),
    install_requires=[
        "Flask==1.1.1",
        "Flask-Migrate==2.5.2",
        "Flask-SQLAlchemy==2.4.1",
        "SQLAlchemy==1.3.13",
        "psycopg2",
        "requests",
        "waitress==2.1.1",
    ],
)
