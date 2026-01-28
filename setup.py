"""Setup configuration for SmolPet"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smolpet",
    version="0.1.0",
    author="Cuchu59",
    description="A little Python project to challenge myself and gift my girlfriend something good",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cuchu59/SmolPet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "smolpet=smolpet.main:main",
        ],
    },
)
