#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import warnings
from pkgutil import find_loader


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

version = {}
with open("arosics/version.py") as version_file:
    exec(version_file.read(), version)

requirements = ['numpy', 'gdal', 'shapely', 'scikit-image', 'matplotlib', 'geopandas', 'geoarray>=0.8.17',
                'py_tools_ds>=0.14.12', 'plotly', 'cmocean', 'six', 'folium>=0.6.0', 'geojson'
                # 'pykrige'  # conda install --yes -c conda-forge pykrige
                # 'pyfftw', # conda install --yes -c conda-forge pyfftw=0.10.4 ; \
                # 'basemap', # conda install --yes -c conda-forge basemap; \
                ]

setup_requirements = [
    'setuptools'
]

test_requirements = requirements + ['coverage', 'nose', 'nose-htmloutput', 'rednose']

setup(
    name='arosics',
    version=version['__version__'],
    description="An Automated and Robust Open-Source Image Co-Registration Software for Multi-Sensor Satellite Data",
    long_description=readme + '\n\n' + history,
    author="Daniel Scheffler",
    author_email='daniel.scheffler@gfz-potsdam.de',
    url='https://gitext.gfz-potsdam.de/danschef/arosics',
    packages=find_packages(),
    include_package_data=True,
    scripts=["bin/arosics_cli.py"],
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords=['arosics', 'image co-registration', 'geometric pre-processing', 'remote sensing', 'sensor fusion'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)


# check for pyfftw
if not find_loader('pyfftw'):
    warnings.warn('You need to install pyfftw manually (see https://pypi.python.org/pypi/pyFFTW) for speeding up '
                  'the computation. It is not automatically installed.')

# check for basemap
if not find_loader('mpl_toolkits.basemap'):
    warnings.warn('You need to install basemap manually if you want to plot maps (see www./matplotlib.org/basemap). '
                  'It is not automatically installed.')

# check for pykrige
if not find_loader('pykrige'):
    warnings.warn('You need to install pykrige manually if you want to interpolate tie point grids produced by AROSICS '
                  '(see https://github.com/bsmurphy/PyKrige). It is not automatically installed.')
