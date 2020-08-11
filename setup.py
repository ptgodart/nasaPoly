from setuptools import setup

setup(
    name="nasaPoly",
    version="0.0.1",
    author="Peter Godart",
    author_email="ptgodart@mit.edu",
    description="Python interface to NASA thermodynamics polynomial fits",
    long_description=open('README.md').read(),
    url="https://github.com/ptgodart/nasaPoly.git",
    packages=['nasaPoly',],
    python_requires='>=3.6',
)
