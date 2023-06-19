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
    
    "numpy>=1.24",

    "typing_extensions>=4.6"
]


QUALITY_REQUIRE = []

TEMPLATE_REQUIRE = [
    # We use cookiecutter to generate task templates
    "cookiecutter>=2.1"
]

TESTS_REQUIRE = [
    # Use PyTest as our test framework
    "pytest>=7.3",
]

EXTRAS_REQUIRE = {
    "dev": TESTS_REQUIRE + QUALITY_REQUIRE,
    "tests": TESTS_REQUIRE,
    "quality": QUALITY_REQUIRE,
    "template": TEMPLATE_REQUIRE,
}


setup(
    name="genbench",
    version="0.0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts": [
            "genbench-cli = genbench.cli.genbench_cli:cli",
        ],
    },
)
