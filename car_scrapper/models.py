"""
Modèles de données pour le car scrapper
"""

from dataclasses import dataclass
from typing import Optional


class Car:
    """
    Classe représentant une voiture
    """
    def __init__(self, make: str, model: str, year: int, price: int, mileage: int, fuel: str, location: str, options: list, detail_url: str = ""):
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.mileage = mileage
        self.fuel = fuel
        self.location = location
        self.options = options
        self.detail_url = detail_url
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.fuel}) - ${self.price:,} - {self.mileage:,} km - {self.location} - URL: {self.detail_url}"
    
    def __repr__(self):
        return self.__str__()


@dataclass
class PageInfo:
    """
    Informations de pagination
    """
    current_page: int
    total_pages: int
    next_page_url: Optional[str] = None
    previous_page_url: Optional[str] = None 