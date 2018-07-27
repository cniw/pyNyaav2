from setuptools import setup
import pyNyaav2

setup(setup_cfg=True,
entry_points = {
    'console_scripts': ['nyaav2=pyNyaav2.command:main']
})
