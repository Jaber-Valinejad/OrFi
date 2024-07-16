from setuptools import setup, find_packages

setup(
    name='my_project',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
'transformers',
'sentence-transformers',
'pandas',
'ast',
'itertools',
'nltk',
're',
'spacy',
'torch',
'tqdm',
'time',
'datetime',
'random',
'numpy',
'math'
    ],
)
