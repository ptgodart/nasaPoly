from setuptools import setup

setup(
    name="nasaPoly",
    version="0.0.1",
    author="Peter Godart",
    author_email="ptgodart@mit.edu",
    description="Python interface to NASA thermodynamics polynomial fits",
    url="https://github.com/ptgodart/nasaPoly.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
