from setuptools import setup, find_packages

with open('README.md', 'r') as f:
	long_description = f.read()

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
	name='website_monitor',
	packages=find_packages(),
	entry_points={'console_scripts': ['monitor = website_monitor.__main__:main', 'monitor = website_monitor.__main__:main']},
	version='1.0.0',
	description='Simple CLI tool to monitor websites\' availabilities and performances',
	long_description=long_description,
	py_modules=['website_monitor'],
	install_requires=requirements,
	author='Mathis Batoul',
	author_email='mathis.batoul@polytechnique.edu'
)
