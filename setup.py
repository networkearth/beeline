from setuptools import setup, find_packages

setup(
    name="beeline",
    version="0.0.1",
    author="Marcel Gietzmann-Sanders",
    author_email="marcelsanders96@gmail.com",
    packages=find_packages(include=["beeline", "beeline*"]),
    install_requires=[],
)
