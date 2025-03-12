"""
Setup script for the Universal File Converter
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="universal-file-converter",
    version="1.0.0",
    author="NamoVize",
    author_email="contact@example.com",
    description="A powerful application that converts between various file formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NamoVize/universal-file-converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "file-converter=src.main:main",
        ],
    },
)