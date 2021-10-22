from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.md')) as f:
    readme = f.read()

setup(
    name             = 'ants_n4biasfieldcorrection',
    version          = '0.2.7.2',
    description      = 'ANTs N4 Bias Field Correction',
    long_description = readme,
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/pl-ANTs_N4BiasFieldCorrection',
    packages         = ['bfc'],
    install_requires = ['chrisapp'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'bfc = bfc.__main__:main'
            ]
        }
)
