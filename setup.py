from setuptools import setup, find_packages

setup(
    name='alerter',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['alerter = alerter.main:main']
    }
)
