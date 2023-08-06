from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="gizoogle_py",
    version="1.0.1",
    description="Python wrapper for gizoogle and textilizer.",
    url="https://github.com/chafla/gizoogle-py",
    author="chafla",
    license="MIT",
    keywords="gizoogle text fun link",
    install_requires=requirements,
    packages=find_packages(),
)
