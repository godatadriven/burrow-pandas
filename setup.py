from setuptools import setup
from os import path


def load_readme():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name='burrowpandas',
    version='0.0.1',
    author=['Matthijs Brouns', 'Vincent D. Warmerdam'],
    python_requires='>=3.6',
    install_requires=['pandas>=0.23.0', 'pytest>=3.8.0', 'numpy>=1.15.0'],
    tests_require=['pandas>=0.23.0', 'pytest>=3.8.0', 'numpy>=1.15.0']
)
