from setuptools import setup, find_packages

setup(
    name='OrFi',
    version='0.1',
    packages=find_packages(where='OrFi'),  # Automatically find packages in 'src'
    package_dir={'': 'OrFi'},  # Specify that packages are under the 'src' directory
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
