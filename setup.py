from setuptools import setup

setup(
    # Application name:
    name="Lig",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Quentin Guilloteau",
    author_email="Quentin.Guilloteau@grenoble-inp.org",

    # Packages
    packages=["app"],

    # Include additional files into the package
    # include_package_data=True,
    entry_points={
        'console_scripts': ['lig=app.lig:main'],
    },

    # Details
    url="https://github.com/GuilloteauQ/lig_annuaire",

    #
    # license="LICENSE.txt",
    description="Lig annuaire from the Command line",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
      "requests",
      "beautifulsoup4",
      "pybase64",
      "tabulate"
    ]
)
