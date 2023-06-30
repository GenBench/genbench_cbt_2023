import os
from pathlib import Path

from setuptools import setup, find_packages

REQUIRED_PKGS = [
    # We use Click to power our command line interface
    "Click>=8.1",
    # Jsonnet is used as a format for task configs
    "jsonnet>=0.20",
    # dataclass_factory is used to convert jsonnet to dataclasses
    "dataclass_factory>=2.16",
    # We use datasets to load data from HuggingFace datasets
    "datasets>=2.13",
    # HuggingFace Evaluate is used for metrics
    "evaluate>=0.4",
    # Scikit-learn is needed for some of HF's metrics
    "scikit-learn",
    # Numpy is needed for some of HF's metrics
    "numpy",
    "typing_extensions>=4.6",
]


QUALITY_REQUIRE = [
    # We use black to format our code
    "black~=23.3",
    # We use isort to sort our imports
    "isort~=5.12",
    # We use flake8 to lint our code
    "flake8~=6.0",
]

TEMPLATE_REQUIRE = [
    # We use cookiecutter to generate task templates
    "cookiecutter>=2.1"
]

TESTS_REQUIRE = [
    # Use PyTest as our test framework
    "pytest>=7.3",
]

EXTRAS_REQUIRE = {
    "dev": TESTS_REQUIRE + QUALITY_REQUIRE + TEMPLATE_REQUIRE,
    "tests": TESTS_REQUIRE,
    "quality": QUALITY_REQUIRE,
    "template": TEMPLATE_REQUIRE,
}


def get_template_data_files():
    data_files = []
    start_point = Path("templates")
    for root, dirs, files in os.walk(start_point):
        root_files = [os.path.join(root, i) for i in files]
        data_files.append((root, root_files))

    print(data_files)
    return data_files


setup(
    name="genbench",
    version="0.0.1.dev0",
    description="A collaborative generalisation benchmark for NLP",
    long_description=open("README.md", encoding="utf-8").read(),
    author="The GenBench Team",
    author_email="genbench@googlegroups.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "genbench": ["tasks/**/*.json", "tasks/**/*.jsonnet", "tasks/**/*.md"]
    },
    include_package_data=True,
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.8.0",
    entry_points={"console_scripts": ["genbench-cli = genbench.cli.genbench_cli:cli"]},
)
