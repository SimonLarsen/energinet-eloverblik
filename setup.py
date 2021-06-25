from setuptools import setup, find_packages
import eloverblik


setup(
    name="eloverblik",
    description="Python wrapper for the Eloverblik.dk API.",
    version=eloverblik.__version__,
    author="Simon J. Larsen",
    author_email="SLN@energinet.dk",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
)
