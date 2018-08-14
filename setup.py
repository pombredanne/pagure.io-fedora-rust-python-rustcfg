from setuptools import setup, find_packages

import rustcfg

setup(
    name='rustcfg',
    version=rustcfg.__version__,
    description='Rust cfg expression parser in python',
    long_description=open('README.md').read(),
    author='Zbigniew Jędrzejewski-Szmek',
    author_email='zbyszek@in.waw.pl',
    license='LGPL-2.1+',
    url='https://pagure.io/fedora-rust/python-rustcfg',
    packages=find_packages(),
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Library Public License v2.1 or later (LGPLv2+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
