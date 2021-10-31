#!/usr/bin/python3
"""Setup
"""
from setuptools import find_packages
from distutils.core import setup

version = "0.1.0"

with open('ReadMe.md') as f:
    long_description = f.read()

setup(name='ofxstatement-de-ing',
      version=version,
      author="Faha",
      author_email="dev-faha@t-online.de",
      url="https://github.com/fabolhak/ofxstatement-de-ing",
      description=("OFXStatement plugin for ING (Germany / Deutschland)"),
      long_description=long_description,
      license="GPLv3",
      keywords=["ofx", "banking", "statement"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU Affero General Public License v3'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=["ofxstatement", "ofxstatement.plugins"],
      entry_points={
          'ofxstatement':
          ['ingde = ofxstatement.plugins.ingde:IngDePlugin']
          },
      extras_require={'test': ["mock", "pytest", "pytest-cov"]},
      tests_require=["mock"],
      include_package_data=True,
      zip_safe=True
      )
