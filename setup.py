from setuptools import setup

setup(
    name='my_project',
    version='0.1',
    packages=["src"]
    install_requires=[
        'transformers',
        'sentence-transformers',
        'pandas',
        'nltk',
        'spacy',
        'torch',
        'tqdm',
        'numpy'
    ],
)
