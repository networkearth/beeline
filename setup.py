from setuptools import setup, find_packages

setup(
    name="beeline",
    version="0.0.1",
    author="Marcel Gietzmann-Sanders",
    author_email="marcelsanders96@gmail.com",
    packages=find_packages(include=["beeline", "beeline*"]),
    install_requires=[
        "click==8.1.7",
        "boto3==1.35.50",
    ],
    entry_points={
        "console_scripts": [
            "beeline = beeline.cli:cli",
        ]
    },
)
