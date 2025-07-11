"""
Setup script pour le paquet car_scrapper
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="car_scrapper",
    version="1.0.0",
    author="Car Scrapper Team",
    author_email="contact@carscrapper.com",
    description="Un outil de scraping pour les sites de vente de voitures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/car_scrapper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "car-scrapper=car_scrapper.cli:main",
        ],
    },
) 