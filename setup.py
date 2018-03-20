from setuptools import setup, find_packages

setup(
    name='alerter',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['alerter = alerter.main:main']
    },
    install_requires=[
        "aiodns==1.1.1",
        "aiohttp==3.0.9",
        "aiofiles==0.3.2",
        "aiotg==0.9.8",
    ]
)
