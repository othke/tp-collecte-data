"""
Serveur API pour le car scrapper
"""

from car_scrapper import CarAPI
import argparse


def main():
    """Lance le serveur API"""
    parser = argparse.ArgumentParser(
        description="Serveur API pour Car Scrapper"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Adresse d'écoute (défaut: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port d'écoute (défaut: 5000)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Mode debug Flask"
    )
    
    parser.add_argument(
        "--db-path",
        type=str,
        default="cars.db",
        help="Chemin vers la base de données (défaut: cars.db)"
    )
    
    args = parser.parse_args()
    
    # Créer et lancer l'API
    api = CarAPI(db_path=args.db_path)
    
    print(f"🚀 Serveur API démarré sur http://{args.host}:{args.port}")
    print(f"📊 Base de données: {args.db_path}")
    print(f"🔗 Endpoints disponibles:")
    print(f"   GET /api/cars - Liste des voitures avec filtres")
    print(f"   GET /api/cars/<id> - Détails d'une voiture")
    print(f"   GET /api/stats - Statistiques")
    print()
    
    api.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main() 