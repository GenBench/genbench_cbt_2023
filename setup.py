from setuptools import setup, find_packages

REQUIRED_PKGS = [
    # We use Click to power our command line interface
    "Click>=8.1",

    # We use cookiecutter to generate task templates
    "cookiecutter>=2.1"
]


QUALITY_REQUIRE = []

TEMPLATE_REQUIRE = []

TESTS_REQUIRE = []

EXTRAS_REQUIRE = {
    "dev": TESTS_REQUIRE + QUALITY_REQUIRE,
    "tests": TESTS_REQUIRE,
    "quality": QUALITY_REQUIRE,
    "template": TEMPLATE_REQUIRE,
}


setup(
    name="genbench",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        "console_scripts": [
            "genbench-cli = genbench.cli.genbench_cli:cli",
        ],
    },
)
