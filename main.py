"""
Script principal pour le car scrapper
"""

from car_scrapper import AlbiScraper


def main():
    """Fonction principale"""
    scraper = AlbiScraper()
    scraper.scrap_from_page(1, 1)
    
    # Afficher toutes les voitures de la base de données
    print("\n" + "="*50)
    scraper.display_all_cars_from_db()


if __name__ == "__main__":
    main() 