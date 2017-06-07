from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='argdown',
    # semver
    version='1.0.0',
    description='Markdown export for the argparse module',
    long_description=long_description,
    url='https://github.com/9999years/argdown',
    author='Rebecca Turner',
    author_email='',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Markup'
    ],

    keywords='markdown argparse',
    packages=find_packages(),

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'argdown=argdown.argdown:console',
        ],
    }
)
