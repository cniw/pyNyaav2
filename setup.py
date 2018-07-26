from setuptools import setup, find_packages
from pyNyaav2 import __author__, __version__, __email__
import codecs

def longdesc():
    with open('README.md') as f:
        return str(f.read())

with open('requirements.txt') as ree:
    requirements = [re1 for re1 in ree.read().splitlines() if re1]

setup(name='pyNyaav2',
version=__version__,
license='MIT',

packages=find_packages(),
author=__author__,
author_email=__email__,
keywords='nyaa, torrent, api, python, nyaa.si',
description='Python Nyaav2 API Wrapper',
long_description=longdesc(),
url='https://github.com/noaione/pyNyaav2',
download_url='https://github.com/noaione/pyNyaav2/tarball/master',
include_package_data=True,
zip_safe=False,

install_requires=requirements
)
