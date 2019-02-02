from setuptools import setup, find_packages

setup(
    name="advent-of-code-wim",
    version="0.1",
    description="Wim's solutions for https://adventofcode.com/",
    url="https://github.com/wimglenn/advent-of-code",
    author="Wim Glenn",
    author_email="hey@wimglenn.com",
    license="WTFPL",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    install_requires=[
        "advent-of-code-data >= 0.8.0",
        "anytree",
        "bidict",
        "numpy",
        "parse",
        "scipy",
        "fields",
        "networkx",
        "wimpy",
    ],
    packages=find_packages(),
    entry_points={
        "adventofcode.user": ["wim = aoc_wim:plugin"],
    },
)