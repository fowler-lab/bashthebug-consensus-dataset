from setuptools import setup

with open("README.md", "r") as f:
    README = f.read()

setup(
    install_requires=[
        "numpy >= 1.21.2",
        "pandas >= 1.3.3",
        "matplotlib >= 3.4.1",
        "scipy >= 1.7.0"],
    name='bashthebug-consensus-dataset',
    version='1.0',
    author='Philip W Fowler',
    author_email="philip.fowler@ndm.ox.ac.uk",
    description="The BashTheBug dataset for finding the optimal consensus method",
    long_descriptions=README,
    url="https://github.com/fowler-lab/bashthebug-consensus-dataset",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"],
    python_requires='>=3.8',
    license="MIT, see LICENSE.md",
    zip_safe=False
)
