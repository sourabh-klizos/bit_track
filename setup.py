from setuptools import setup, find_packages

setup(
    name="bit_track",
    version="0.1.0",
    packages=find_packages(),  # Auto-detects 'bit_track' package
    install_requires=[],
    entry_points={
        "console_scripts": [
            "bit_track=bit_track:main",  # Correctly points to bit_track/main.py
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