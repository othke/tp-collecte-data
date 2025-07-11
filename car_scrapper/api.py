"""
API REST pour le car scrapper
"""

from flask import Flask, request, jsonify
from .database import CarDatabase
from .models import Car
import json


class CarAPI:
    """
    API REST pour les voitures
    """
    def __init__(self, db_path: str = "cars.db"):
        self.app = Flask(__name__)
        self.database = CarDatabase(db_path)
        self.setup_routes()
    
    def setup_routes(self):
        """Configure les routes de l'API"""
        
        @self.app.route('/api/cars', methods=['GET'])
        def get_cars():
            """Récupère les voitures avec filtres, pagination et tri"""
            try:
                # Paramètres de pagination
                page = request.args.get('page', 1, type=int)
                per_page = min(request.args.get('per_page', 20, type=int), 50)
                
                # Paramètres de recherche
                make = request.args.get('make', '').strip()
                model = request.args.get('model', '').strip()
                fuel = request.args.get('fuel', '').strip()
                price_lt = request.args.get('price_lt', type=int)
                price_gt = request.args.get('price_gt', type=int)
                year_lt = request.args.get('year_lt', type=int)
                year_gt = request.args.get('year_gt', type=int)
                
                # Paramètres de tri
                sort_by = request.args.get('sort_by', 'id')
                sort_order = request.args.get('sort_order', 'asc')
                
                # Préparer les filtres
                filters = {
                    'make': make if make else None,
                    'model': model if model else None,
                    'fuel': fuel if fuel else None,
                    'price_lt': price_lt,
                    'price_gt': price_gt,
                    'year_lt': year_lt,
                    'year_gt': year_gt
                }
                
                # Récupérer les voitures avec filtres, tri et pagination directement en SQL
                cars, total_count = self.database.get_cars_with_filters(
                    filters=filters,
                    sort_by=sort_by,
                    sort_order=sort_order,
                    page=page,
                    per_page=per_page
                )
                
                # Convertir en dictionnaires pour JSON
                cars_data = []
                for car in cars:
                    cars_data.append({
                        'id': getattr(car, 'id', None),
                        'make': car.make,
                        'model': car.model,
                        'year': car.year,
                        'price': car.price,
                        'mileage': car.mileage,
                        'fuel': car.fuel,
                        'location': car.location,
                        'options': car.options,
                        'detail_url': car.detail_url
                    })
                
                return jsonify({
                    'cars': cars_data,
                    'pagination': {
                        'page': page,
                        'per_page': per_page,
                        'total_count': total_count,
                        'total_pages': (total_count + per_page - 1) // per_page
                    },
                    'filters': {
                        'make': make,
                        'model': model,
                        'fuel': fuel,
                        'price_lt': price_lt,
                        'price_gt': price_gt,
                        'year_lt': year_lt,
                        'year_gt': year_gt
                    },
                    'sorting': {
                        'sort_by': sort_by,
                        'sort_order': sort_order
                    }
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/cars/<int:car_id>', methods=['GET'])
        def get_car(car_id):
            """Récupère une voiture spécifique par ID"""
            try:
                car = self.database.get_car_by_id(car_id)
                if car:
                    return jsonify({
                        'id': getattr(car, 'id', None),
                        'make': car.make,
                        'model': car.model,
                        'year': car.year,
                        'price': car.price,
                        'mileage': car.mileage,
                        'fuel': car.fuel,
                        'location': car.location,
                        'options': car.options,
                        'detail_url': car.detail_url
                    })
                else:
                    return jsonify({'error': 'Voiture non trouvée'}), 404
                    
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Récupère les statistiques de la base de données"""
            try:
                all_cars = self.database.get_all_cars()
                
                # Statistiques par marque
                makes = {}
                fuels = {'Essence': 0, 'Électrique': 0}
                total_price = 0
                total_mileage = 0
                years = []
                
                for car in all_cars:
                    # Comptage par marque
                    makes[car.make] = makes.get(car.make, 0) + 1
                    
                    # Comptage par carburant
                    fuels[car.fuel] = fuels.get(car.fuel, 0) + 1
                    
                    # Calculs pour moyennes
                    total_price += car.price
                    total_mileage += car.mileage
                    years.append(car.year)
                
                avg_price = total_price / len(all_cars) if all_cars else 0
                avg_mileage = total_mileage / len(all_cars) if all_cars else 0
                avg_year = sum(years) / len(years) if years else 0
                
                return jsonify({
                    'total_cars': len(all_cars),
                    'makes': makes,
                    'fuels': fuels,
                    'averages': {
                        'price': round(avg_price, 2),
                        'mileage': round(avg_mileage, 2),
                        'year': round(avg_year, 1)
                    }
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    

    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
        """Lance le serveur Flask"""
        self.app.run(host=host, port=port, debug=debug) 