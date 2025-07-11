"""
Extracteur de données pour les pages web
"""

import re
from bs4 import BeautifulSoup
from .models import Car


class AlbiPageExtractor:
    """
    Extractor pour Albi.ca
    """
    def __init__(self, html: str, base_url: str):
        self.html = html
        self.base_url = base_url
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.cars = self.parse_cars()
        
    def parse_cars(self):
        """
        Parse les voitures à partir du HTML
        """
        cars = []
        
        # Chercher tous les éléments de voiture (liens avec classe promotion-item)
        car_elements = self.soup.find_all('a', class_='promotion-item')
        
        for car_element in car_elements:
            try:
                # Extraire l'URL de détail
                detail_url = car_element.get('href', '')
                # Si l'URL est relative, la rendre absolue
                if detail_url.startswith('/'):
                    detail_url = f"{self.base_url}{detail_url}"
                
                # Extraire les métadonnées structurées
                name_meta = car_element.find('meta', {'itemprop': 'name'})
                brand_meta = car_element.find('meta', {'itemprop': 'brand'})
                model_meta = car_element.find('meta', {'itemprop': 'model'})
                year_meta = car_element.find('meta', {'itemprop': 'vehicleModelDate'})
                config_meta = car_element.find('meta', {'itemprop': 'vehicleConfiguration'})
                vin_meta = car_element.find('meta', {'itemprop': 'vehicleIdentificationNumber'})
                
                # Extraire le prix
                price_meta = car_element.find('meta', {'itemprop': 'price'})
                price_currency_meta = car_element.find('meta', {'itemprop': 'priceCurrency'})
                
                # Extraire le kilométrage
                km_block = car_element.find('div', class_='km-block')
                
                # Extraire la localisation
                distance_container = car_element.find('div', class_='distance-container')
                
                # Extraire les options
                option_container = car_element.find('div', class_='option-container')
                
                # Traitement des données
                make = brand_meta.get('content', '') if brand_meta else ''
                model = model_meta.get('content', '') if model_meta else ''
                year = int(year_meta.get('content', 0)) if year_meta else 0
                price = int(price_meta.get('content', 0)) if price_meta else 0
                
                # Extraire le kilométrage
                mileage = 0
                if km_block:
                    km_text = km_block.get_text(strip=True)
                    # Extraire les chiffres du texte "62318 km"
                    km_match = re.search(r'(\d+)', km_text)
                    if km_match:
                        mileage = int(km_match.group(1))
                
                # Extraire la localisation
                location = ''
                if distance_container:
                    location_text = distance_container.get_text(strip=True)
                    # Nettoyer le texte de localisation
                    location = location_text.replace('\n', ' ').strip()
                
                # Extraire les options
                options = []
                if option_container:
                    option_items = option_container.find_all('li')
                    options = [item.get_text(strip=True) for item in option_items]
                
                # Déterminer le type de carburant
                fuel = 'Essence'  # Par défaut
                # Chercher l'indicateur de véhicule électrique
                overlay_gouv_rebate = car_element.find('div', class_='overlay-gouv-rebate')
                if overlay_gouv_rebate:
                    overlay_text = overlay_gouv_rebate.get_text(strip=True)
                    if 'Véhicule électrique' in overlay_text or 'électrique' in overlay_text.lower():
                        fuel = 'Électrique'
                
                # Créer l'objet Car
                car = Car(
                    make=make,
                    model=model,
                    year=year,
                    price=price,
                    mileage=mileage,
                    fuel=fuel,
                    location=location,
                    options=options,
                    detail_url=detail_url
                )
                
                cars.append(car)
                
            except Exception as e:
                print(f"Erreur lors du parsing d'une voiture: {e}")
                continue
        
        return cars 