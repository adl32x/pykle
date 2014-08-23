from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
  name = 'pykle',
  packages = ['pykle'],
  version = '0.0.1',
  description = 'A static website generator written in Python',
  author = 'Andreas Lindroos',
  author_email = 'andreas.lindroos@gmail.com',
  url = 'https://github.com/adl32x/pykle',
  scripts=['pykle/pykle.py'],
  #download_url = 'https://github.com/adl32x/pykle/tarball/0.0.1',
  keywords = ['static', 'website', 'generator'],
  install_requires=required,
  classifiers = []
)
