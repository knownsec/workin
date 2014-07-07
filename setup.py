#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

install_requires = (
)

setup(
    name="workin",
    version="0.1",
    description="Work in tornado",
    author="Alvin Yao",
    author_email='yao.angellin@gmail.com',
    url="http://alvinyao.github.com/",
    license="MIT",
    include_package_data=True,
    install_requires=install_requires,
    packages=find_packages(),
)
