#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGES.rst") as history_file:
    history = history_file.read()

setup(
    author="riscLOG Solution GmbH",
    author_email="info@risclog.de",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: German",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="The CryptographyManager is a tool designed to securely encrypt and decrypt messages and data. It uses modern encryption techniques to protect confidential information.",
    install_requires=[
        # Add your dependencies here
        "risclog.logging",
        "cryptography",
    ],
    extras_require={
        "docs": [
            "Sphinx",
        ],
        "test": [
            "pytest-cache",
            "pytest-cov",
            "pytest-flake8",
            "pytest-rerunfailures",
            "pytest-sugar",
            "pytest-asyncio",
            "pytest",
            "coverage",
            # https://github.com/PyCQA/flake8/issues/1419#issuecomment-947243876
            "flake8<4",
        ],
    },
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="risclog.cryptography",
    name="risclog.cryptography",
    packages=find_packages("src"),
    namespace_packages=["risclog"],
    package_dir={"": "src"},
    url="https://github.com/risclog-solution/risclog.cryptography",
    version="1.2.dev0",
    zip_safe=False,
)
