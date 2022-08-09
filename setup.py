from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path
import subprocess

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    # $ pip install pollock
    name='enrichrpy',
    version='0.0.1',
    description='A tool for gene set enrichment (GSEA) plots and analysis in Python. Built on top of Enrichr API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/estorrs/enrichrpy',
    author='Erik Storrs',
    author_email='epstorrs@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    keywords='GSEA gene set enrichment plot figure analysis enrichr',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'altair',
        'requests',
    ],
    include_package_data=True,

    entry_points={
        'console_scripts': [
        ],
    },
)
