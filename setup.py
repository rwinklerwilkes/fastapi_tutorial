from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(name='FastAPI Sample Project',
      version = '0.0.1',
      description= 'Sample project to learn FastAPI library',
      long_description=long_description,
      author = 'Rich Winkler',
      packages = find_packages(),
      python_requires = '>=3.10'
      )