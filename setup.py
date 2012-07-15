from setuptools import setup, find_packages
import os

version = '0.1'

long_description = (
    open('README.md').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='msongs.migration',
      version=version,
      description="Import Million Song Dataset to Mongo",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Marco Mariani',
      author_email='birbag@gmail.com',
      url='https://github.com/mmariani/msongs.migration',
      license='gpl',
      packages=find_packages(),
      namespace_packages=['msongs'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pymongo',
          'decorator',
          'h5py',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      msongs-import = msongs.migration.h5import:main
      """,
      )
