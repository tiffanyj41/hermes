from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import os
import sys
import re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests'] # tests if rename src to hermes
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='hermes',
    version=find_version('hermes', '__init__.py'),
    url='http://github.com/lab41/hermes/',
    license='Apache Software License',
    author='Lab 41',
    description='Exploration of Recommender Systems',
    long_description=long_description,
    tests_require=['pytest'],
    install_requires=['click',
                     ],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'hermes = hermes.hermesctl:main',
            ],
        },
    py_modules=['hermes'],
    #scripts=['scripts/somescript.py'],
    packages=['hermes', 'hermes.modules', 'hermes.metrics', 'hermes.utils'],
    include_package_data=True,
    platforms='any',
    test_suite='tests.test_hermes.py',
    zip_safe=False,
    #package_data={'hermes': ['templates/**', 'static/*/*']}, 
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 1',
        'Natural Language :: English',
        'Environment :: Spark Environment',
        'Intended Audience :: Developers, Data Scientists',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MAC OS X',
        'Topic :: Recommender System',
        ],
    extras_require={
        'testing': ['pytest'],
      }
)
