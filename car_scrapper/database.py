"""
Gestionnaire de base de données pour les voitures
"""

import sqlite3
import json
from .models import Car


class CarDatabase:
    """
    Gestionnaire de base de données pour les voitures
    """
    def __init__(self, db_path: str = "cars.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données et crée la table si elle n'existe pas"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Car (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    make TEXT NOT NULL,
                    model TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    mileage INTEGER NOT NULL,
                    fuel TEXT NOT NULL,
                    location TEXT NOT NULL,
                    options TEXT NOT NULL,
                    detail_url TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def car_exists(self, detail_url: str) -> bool:
        """Vérifie si une voiture existe déjà dans la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Car WHERE detail_url = ?", (detail_url,))
            return cursor.fetchone()[0] > 0
    
    def insert_car(self, car: Car) -> bool:
        """Insère une nouvelle voiture dans la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Car (make, model, year, price, mileage, fuel, location, options, detail_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    car.make,
                    car.model,
                    car.year,
                    car.price,
                    car.mileage,
                    car.fuel,
                    car.location,
                    json.dumps(car.options),
                    car.detail_url
                ))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # L'URL existe déjà, on met à jour
            return self.update_car(car)
        except Exception as e:
            print(f"Erreur lors de l'insertion: {e}")
            return False
    
    def update_car(self, car: Car) -> bool:
        """Met à jour une voiture existante dans la base de données"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE Car 
                    SET make = ?, model = ?, year = ?, price = ?, mileage = ?, 
                        fuel = ?, location = ?, options = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE detail_url = ?
                ''', (
                    car.make,
                    car.model,
                    car.year,
                    car.price,
                    car.mileage,
                    car.fuel,
                    car.location,
                    json.dumps(car.options),
                    car.detail_url
                ))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            return False
    
    def get_all_cars(self) -> list[Car]:
        """Récupère toutes les voitures de la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT make, model, year, price, mileage, fuel, location, options, detail_url FROM Car")
            rows = cursor.fetchall()
            
            cars = []
            for row in rows:
                options = json.loads(row[7]) if row[7] else []
                car = Car(
                    make=row[0],
                    model=row[1],
                    year=row[2],
                    price=row[3],
                    mileage=row[4],
                    fuel=row[5],
                    location=row[6],
                    options=options,
                    detail_url=row[8]
                )
                cars.append(car)
            
            return cars
    
    def get_car_count(self) -> int:
        """Retourne le nombre total de voitures dans la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Car")
            return cursor.fetchone()[0]
    
    def get_car_by_id(self, car_id: int) -> Car:
        """Récupère une voiture par son ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, make, model, year, price, mileage, fuel, location, options, detail_url 
                FROM Car WHERE id = ?
            """, (car_id,))
            row = cursor.fetchone()
            
            if row:
                options = json.loads(row[8]) if row[8] else []
                car = Car(
                    make=row[1],
                    model=row[2],
                    year=row[3],
                    price=row[4],
                    mileage=row[5],
                    fuel=row[6],
                    location=row[7],
                    options=options,
                    detail_url=row[9]
                )
                # Ajouter l'ID à l'objet car
                car.id = row[0]
                return car
            
            return None
    
    def get_cars_with_filters(self, filters: dict, sort_by: str = 'id', sort_order: str = 'asc', 
                             page: int = 1, per_page: int = 20) -> tuple[list[Car], int]:
        """
        Récupère les voitures avec filtres, tri et pagination directement en SQL
        Retourne (voitures, total_count)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Construire la requête SQL avec filtres
            where_conditions = []
            params = []
            
            # Filtres
            if filters.get('make'):
                where_conditions.append("LOWER(make) LIKE LOWER(?)")
                params.append(f"%{filters['make']}%")
            
            if filters.get('model'):
                where_conditions.append("LOWER(model) LIKE LOWER(?)")
                params.append(f"%{filters['model']}%")
            
            if filters.get('fuel'):
                where_conditions.append("LOWER(fuel) LIKE LOWER(?)")
                params.append(f"%{filters['fuel']}%")
            
            if filters.get('price_lt') is not None:
                where_conditions.append("price < ?")
                params.append(filters['price_lt'])
            
            if filters.get('price_gt') is not None:
                where_conditions.append("price > ?")
                params.append(filters['price_gt'])
            
            if filters.get('year_lt') is not None:
                where_conditions.append("year < ?")
                params.append(filters['year_lt'])
            
            if filters.get('year_gt') is not None:
                where_conditions.append("year > ?")
                params.append(filters['year_gt'])
            
            # Construire la clause WHERE
            where_clause = ""
            if where_conditions:
                where_clause = "WHERE " + " AND ".join(where_conditions)
            
            # Validation du champ de tri
            valid_sort_fields = ['id', 'make', 'model', 'year', 'price', 'mileage', 'fuel', 'location']
            if sort_by not in valid_sort_fields:
                sort_by = 'id'
            
            # Construire la clause ORDER BY
            order_clause = f"ORDER BY {sort_by} {sort_order.upper()}"
            
            # Requête pour compter le total
            count_query = f"SELECT COUNT(*) FROM Car {where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Requête pour récupérer les données avec pagination
            limit = per_page
            offset = (page - 1) * per_page
            
            data_query = f"""
                SELECT id, make, model, year, price, mileage, fuel, location, options, detail_url 
                FROM Car {where_clause} {order_clause} LIMIT ? OFFSET ?
            """
            cursor.execute(data_query, params + [limit, offset])
            rows = cursor.fetchall()
            
            # Convertir les résultats en objets Car
            cars = []
            for row in rows:
                options = json.loads(row[8]) if row[8] else []
                car = Car(
                    make=row[1],
                    model=row[2],
                    year=row[3],
                    price=row[4],
                    mileage=row[5],
                    fuel=row[6],
                    location=row[7],
                    options=options,
                    detail_url=row[9]
                )
                car.id = row[0]
                cars.append(car)
            
            return cars, total_count 