from setuptools import setup, find_packages

setup(
    name='src',
    version='0.1',
    packages=find_packages(where='src'),  # Automatically find packages in 'src'
    package_dir={'': 'src'},  # Specify that packages are under the 'src' directory
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
