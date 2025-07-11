"""
Scraper principal pour les sites de vente de voitures
"""

from tabulate import tabulate
from .models import Car
from .database import CarDatabase
from .extractor import AlbiPageExtractor
from .navigator import AlbiNavigator


class AlbiScraper:
    """
    Scraper pour Albi.ca
    """
    def __init__(self, db_path: str = "cars.db"):
        self.navigator = AlbiNavigator()
        self.database = CarDatabase(db_path)


    def display_cars(self, cars: list[Car]):
        """
        Affiche les voitures sous forme de cartes avec tabulate
        """
        if not cars:
            print("Aucune voiture trouvée")
            return
        
        print(f"\n{len(cars)} voitures trouvées:")
        
        for i, car in enumerate(cars, 1):
            print(f"\n--- Voiture #{i} ---")
            
            # Préparer les données pour la carte
            card_data = [
                ["Marque", car.make],
                ["Modèle", car.model],
                ["Année", str(car.year)],
                ["Prix", f"${car.price:,}"],
                ["Kilométrage", f"{car.mileage:,} km"],
                ["Carburant", car.fuel],
                ["Localisation", car.location],
                ["URL", car.detail_url],
                ["Options", ", ".join(car.options) if car.options else "Aucune"]
            ]
            
            # Afficher la carte
            print(tabulate(card_data, tablefmt="simple", colalign=("right", "left")))
            print()

    def scrap_from_page(self, start_page_number: int = 1, number_of_pages_to_scrap: int = 2):
        # Vérifier si les exigences de scraping sont conformes avec le nombre de pages disponibles
        page_info = self.navigator.get_page_infos()
        total_pages = page_info.total_pages
        
        if total_pages == 0:
            print("Aucune page trouvée")
            return
        
        if total_pages < start_page_number:
            print(f"Le numéro de page de départ ({start_page_number}) est supérieur au nombre total de pages ({total_pages})")
            return
        
        if start_page_number + number_of_pages_to_scrap > total_pages:
            number_of_pages_to_scrap = total_pages - start_page_number + 1
            print(f"Le nombre de pages à scraper dépasse le nombre total de pages, {number_of_pages_to_scrap} pages seront scrapées")
        
        # Scraper les pages suivantes
        total_cars_processed = 0
        total_cars_inserted = 0
        total_cars_updated = 0
        
        for i in range(start_page_number, start_page_number + number_of_pages_to_scrap):
            page_url = self.navigator.get_inventory_url(i)
            self.navigator.go_to_page(page_url)
            content = self.navigator.get_html()
            extractor = AlbiPageExtractor(content, self.navigator.base_url)
            
            # Sauvegarder les voitures dans la base de données
            for car in extractor.cars:
                total_cars_processed += 1
                if self.database.car_exists(car.detail_url):
                    if self.database.update_car(car):
                        total_cars_updated += 1
                        print(f"✓ Voiture mise à jour: {car.make} {car.model} ({car.fuel})")
                    else:
                        print(f"✗ Erreur lors de la mise à jour: {car.make} {car.model}")
                else:
                    if self.database.insert_car(car):
                        total_cars_inserted += 1
                        print(f"✓ Nouvelle voiture ajoutée: {car.make} {car.model} ({car.fuel})")
                    else:
                        print(f"✗ Erreur lors de l'insertion: {car.make} {car.model}")

        # Afficher le résumé
        print(f"\n=== RÉSUMÉ DU SCRAPING ===")
        print(f"Voitures traitées: {total_cars_processed}")
        print(f"Nouvelles voitures ajoutées: {total_cars_inserted}")
        print(f"Voitures mises à jour: {total_cars_updated}")
        print(f"Total dans la base de données: {self.database.get_car_count()}")
    
    def display_all_cars_from_db(self):
        """Affiche toutes les voitures stockées dans la base de données"""
        cars = self.database.get_all_cars()
        if cars:
            print(f"\n=== TOUTES LES VOITURES EN BASE DE DONNÉES ({len(cars)}) ===")
            self.display_cars(cars)
        else:
            print("Aucune voiture trouvée dans la base de données")
    
    @classmethod
    def display_cars_from_db(cls, db_path: str = "cars.db"):
        """Affiche toutes les voitures d'une base de données sans initialiser le scraper"""
        from .database import CarDatabase
        
        database = CarDatabase(db_path)
        cars = database.get_all_cars()
        
        if cars:
            print(f"\n=== TOUTES LES VOITURES EN BASE DE DONNÉES ({len(cars)}) ===")
            # Créer une instance temporaire juste pour l'affichage
            temp_scraper = cls.__new__(cls)
            temp_scraper.display_cars(cars)
        else:
            print("Aucune voiture trouvée dans la base de données") 