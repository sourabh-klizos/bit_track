

from setuptools import setup, find_packages

setup(
    name="bit_track",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "bit_track=main:main",  # Maps `bit_track` CLI command to `main()`
        ],
    },
    author="Your Name",
    description="A Git-like version control system",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)


# pip install --editable .