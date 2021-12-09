from setuptools import setup, find_packages
import re
from pathlib import Path

here = Path(__file__).parent
version = re.search(
    r'__version__ = "(.+?)"',
    (here / "eloverblik" / "__init__.py").read_text("utf8"),
).group(1)


setup(
    name="eloverblik",
    description="Python wrapper for the Eloverblik.dk API.",
    version=version,
    author="Simon J. Larsen",
    author_email="SLN@energinet.dk",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests", "pandas"],
)
