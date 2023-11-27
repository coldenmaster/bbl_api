from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in bbl_api/__init__.py
from bbl_api import __version__ as version

setup(
	name="bbl_api",
	version=version,
	description="Iot and other machine API",
	author="BBL",
	author_email="wangtao@hbbbl.top",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
