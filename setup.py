from setuptools import setup, find_packages

setup(
    name='function',
    version='0.1',
    packages=find_packages(where='src'),  # Automatically find packages in 'src'
    package_dir={'': 'functions'},  # Specify that packages are under the 'src' directory
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
