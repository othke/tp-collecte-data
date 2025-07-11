"""
Car Scrapper - Un outil de scraping pour les sites de vente de voitures
"""

from .models import Car, PageInfo
from .database import CarDatabase
from .extractor import AlbiPageExtractor
from .navigator import AlbiNavigator
from .scraper import AlbiScraper

__version__ = "1.0.0"
__author__ = "Car Scrapper Team"

__all__ = [
    "Car",
    "PageInfo", 
    "CarDatabase",
    "AlbiPageExtractor",
    "AlbiNavigator",
    "AlbiScraper"
] 