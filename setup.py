from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tgpt",
    version="0.1.0",
    author="Magnus Jansson",
    author_email="mengus00@gmail.com",
    description="TGPT is a CLI interface to OpenAI's GPT models, bringing GPT to the Linux terminal and console",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/indeedion/TGPT",
    packages=find_packages(exclude=("test",)),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'tgpt=tgpt.main:main',
        ],
    },
)

