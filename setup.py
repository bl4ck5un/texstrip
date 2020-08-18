from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='texstrip',
    version='0.1.1',
    description='strip comments from LaTeX sources.',
    license='MIT',
    long_description=long_description,
    url='https://github.com/bl4ck5un/texstrip.py',
    author='Fan Zhang',
    author_email='bl4ck5unxx@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='LaTeX',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['chromalog', 'docopt', 'ply'],
    entry_points={
        'console_scripts': [
            'texstrip=texstrip.__main__:main',
        ],
    },
)