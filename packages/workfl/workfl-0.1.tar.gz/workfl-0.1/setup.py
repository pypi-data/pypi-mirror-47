from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="workfl",
    version="0.1",
    author="Adam Dullage",
    author_email="adam@dullage.com",
    description="A simple flow-diagram markup language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dullage/workfl",
    license="MIT",
    packages=["workfl"],
    install_requires=[],
)
