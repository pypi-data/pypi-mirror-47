from distutils.core import setup
from setuptools import setup, find_packages

import codecs
import os
import re
import sys

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open('requirements.txt', 'r') as req_file:
        requirements = req_file.read()
    install_requires = requirements.splitlines()
except FileNotFoundError as e:
    install_requires = [
        'bokeh',
        'pykube',
        'boto3==1.9.16',
        'botocore==1.12.16',
        'click==7.0',
        'dask==0.19.3',
        'dask[dataframe]==0.19.3',
        'toolz',
        'fastparquet',
        'flask==1.0.2',
        'google-api-core',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth',
        'google-cloud-core',
        'google-cloud-logging',
        'google-cloud-storage',
        'googleapis-common-protos',
        'joblib==0.11',
        'luigi',
        'numpy==1.16.3',
        'pandas==0.23.4',
        'pyarrow==0.11.1',
        'redis==2.10.6',
        'requests',
        's3fs==0.1.6',
        's3transfer==0.1.13',
        'tqdm==4.28.1',
        'urllib3',
        'websocket-client==0.53.0',
        'missingno==0.4.1',
        'deprecated'
    ]

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

setup(
    name='pycarol',
    packages=find_packages(exclude=['docs', 'doc']),
    version=find_version("pycarol", "__init__.py"),
    license='TOTVS',
    description='Carol Python API and Tools',
    author='TotvsLabs',
    maintainer='TOTVS Labs',
    author_email='ops@totvslabs.com',
    url='https://www.carol.ai/',
    keywords=['Totvs', 'Carol.ai', 'AI'],
    install_requires=install_requires,
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],
)
