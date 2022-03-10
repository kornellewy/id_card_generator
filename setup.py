from importlib.metadata import entry_points
from setuptools import find_packages, setup

# pip install pip -e .
setup(
    name="id_card_generator",
    packages=find_packages(exclude=("tests*",)),
    entry_points={"console_scripts": ["id_card_generator=id_card_generator.cli:app"]},
)
