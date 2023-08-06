#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.extension import Extension


# Current Graphbrain version
with open('VERSION', 'r') as version_file:
    VERSION = version_file.read()


# True to enable building extensions using Cython.
# False to build extensions from the C files that were previously
# created by Cython.
USE_CYTHON = False


if USE_CYTHON:
    from Cython.Build import cythonize


if USE_CYTHON:
    ext_modules = [
        Extension('graphbrain.funs', ['graphbrain/funs.pyx'],),
        Extension('graphbrain.hypergraphs.leveldb',
                  ['graphbrain/hypergraphs/leveldb.pyx']),
        Extension('graphbrain.hypergraphs.permutations',
                  ['graphbrain/hypergraphs/permutations.pyx']),
        Extension('graphbrain.parsers.parser_en',
                  ['graphbrain/parsers/parser_en.pyx'])
    ]
    ext_modules = cythonize(ext_modules,
                            compiler_directives={'language_level': '3'})
else:
    ext_modules = [
        Extension('graphbrain.funs', ['graphbrain/funs.c'], ),
        Extension('graphbrain.hypergraphs.leveldb',
                  ['graphbrain/hypergraphs/leveldb.c']),
        Extension('graphbrain.hypergraphs.permutations',
                  ['graphbrain/hypergraphs/permutations.c']),
        Extension('graphbrain.parsers.parser_en',
                  ['graphbrain/parsers/parser_en.c'])
    ]


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='graphbrain',
    version=VERSION,
    author='Telmo Menezes et al.',
    author_email='telmo@telmomenezes.net',
    description='Knowledge System + Natural Language Understanding',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/graphbrain/graphbrain',
    license='MIT',
    keywords=['NLP', 'AI', 'Knowledge Representation', 'Knowledge Systems',
              'Natural Language Understanding', 'Text Analysis', 'Cognition'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Sociology'
    ],
    python_requires='>=3.4',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'termcolor',
        'spacy',
        'asciitree',
        'plyvel',
        'ipython',
        'progressbar2',
        'unidecode'
    ],
    extras_require={
        'dev': [
            'cython',
            'Sphinx',
            'sphinx_rtd_theme'
        ]
    },
    entry_points='''
        [console_scripts]
        graphbrain=graphbrain.__main__:cli
    ''',
    ext_modules=ext_modules,
    test_suite='graphbrain.tests'
)
