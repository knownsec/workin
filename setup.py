#!/usr/bin/env python
# encoding: utf-8

from setuptools import Command, setup, find_packages

install_requires = (
)
    
class run_audit(Command):
    description = "Audit source code with PyFlakes"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        import sys
        try:
            import pyflakes.scripts.pyflakes as flakes
        except ImportError:
            print("Audit requires PyFlakes installed in your system.")
            sys.exit(-1)

        warns = 0
        # Define top-level directories
        dirs = ('workin', )
        for dir in dirs:
            for root, _, files in os.walk(dir):
                for file in files:
                    if file != '__init__.py' and file.endswith('.py'):
                        warns += flakes.checkPath(os.path.join(root, file))
        if warns > 0:
            print("Audit finished with total %d warnings." % warns)
        else:
            print("No problems found in sourcecode.")

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
    cmdclass={'audit': run_audit},
    test_suite='tests'
)
