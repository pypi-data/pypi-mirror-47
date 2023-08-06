from distutils.core import setup

setup(
    name='TDXLib',
    description='a python library for interacting with the TeamDynamix Web API',
    version='0.1.4',
    packages=['tdxlib'],
    url='https://github.com/cedarville-university/tdxlib',
    license='GNU General Public License v3.0',
    long_description='This module provides options for programmatically affectin TDX objects, including tickets, '
                     'people, accounts, assets, and groups.',
    install_requires=['python-dateutil','requests', 'xlrd'],
    python_requires='>=3.6'
)