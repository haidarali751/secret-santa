from setuptools import setup, find_packages

setup(
    name="secret-santa",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "streamlit",
    ],
)