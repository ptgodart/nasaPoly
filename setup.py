from setuptools import setup, find_packages

setup(
    name="nasaPoly",
    version="0.0.1",
    author="Peter Godart",
    author_email="ptgodart@mit.edu",
    description="Python interface to NASA thermodynamics polynomial fits",
    long_description=open('README.md').read(),
    url="https://github.com/ptgodart/nasaPoly.git",
    py_modules=['nasaPoly'],
    packages=find_packages(),
    python_requires='>=3.6',
    package_data={'nasaPoly': ['raw.dat']},
    include_package_data=True,
)
