"""
Interface en ligne de commande pour car_scrapper
"""

import argparse
from . import AlbiScraper


def main():
    """Fonction principale pour l'interface CLI"""
    parser = argparse.ArgumentParser(
        description="Car Scrapper - Outil de scraping pour les sites de vente de voitures"
    )
    
    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="Numéro de la page de départ (défaut: 1)"
    )
    
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Nombre de pages à scraper (défaut: 1)"
    )
    
    parser.add_argument(
        "--db-path",
        type=str,
        default="cars.db",
        help="Chemin vers la base de données (défaut: cars.db)"
    )
    
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Afficher toutes les voitures de la base de données"
    )
    
    args = parser.parse_args()
    
    if args.show_all:
        # Afficher seulement les voitures de la base de données (sans initialiser le scraper)
        AlbiScraper.display_cars_from_db(args.db_path)
    else:
        # Créer le scraper complet pour le scraping
        scraper = AlbiScraper(db_path=args.db_path)
        
        # Scraper les pages
        scraper.scrap_from_page(args.start_page, args.pages)
        
        # Afficher toutes les voitures de la base de données
        print("\n" + "="*50)
        scraper.display_all_cars_from_db()


if __name__ == "__main__":
    main() 