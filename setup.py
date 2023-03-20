import os
from setuptools import setup, find_packages

with open("requirements.txt", "r") as file:
    requirements = [line for line in file.read().splitlines() if line and not line.startswith("#")]

with open(os.path.join("src", "alfred", "VERSION"), "r") as file:
    version = file.read().strip()

with open("README.md") as file:
    readme = file.read()

setup(
    name="alfred",
    version=version,
    description="Alfred - your personal chatbot assistant using OpenAI's GPT technology",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/RHDZMOTA/alfred-gpt",
    author="Rodrigo H. Mota",
    author_email="contact@rhdzmota.com",
    packages=find_packages(where="src"),
    package_dir={
        "": "src"
    },
    package_data={
        "": [
            os.path.join("resources", "assistant_description.txt"),
        ]
    },
    scripts=[
        "bin/alfred"
    ],
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.8.10"
)
