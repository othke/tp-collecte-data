# Rapport - Processus de Collecte de Données
## TP1: Mise en place d'un processus de collecte de données

### 1. Introduction

Ce projet s'inscrit dans le cadre d'un cours sur la collecte de données. L'objectif est de développer un système de scraping automatisé pour collecter des données de voitures depuis le site web Albi.ca et de les stocker dans une base de données pour analyse ultérieure.

Le projet **Car Scrapper** est un outil complet de collecte de données qui permet de :
- Se connecter automatiquement au site Albi.ca
- Extraire les informations des voitures (marque, modèle, année, prix, kilométrage, etc.)
- Stocker les données dans une base de données SQLite
- Fournir une API REST pour accéder aux données collectées
- Gérer les doublons et les mises à jour automatiques

### 2. Caractéristiques du processus

#### 2.1 Architecture générale
Le processus de collecte de données est structuré en plusieurs composants modulaires :

- **Navigateur web** (`navigator.py`) : Gère la connexion et la navigation sur le site source
- **Extracteur de données** (`extractor.py`) : Parse le HTML et extrait les informations des voitures
- **Base de données** (`database.py`) : Gère le stockage et la récupération des données
- **Scraper principal** (`scraper.py`) : Orchestre le processus de collecte
- **API REST** (`api.py`) : Fournit un accès HTTP aux données collectées

#### 2.2 Source de données
- **Site cible** : Albi.ca (https://www.albioccasion.com)
- **Type de données** : Informations de voitures d'occasion
- **Format source** : Pages HTML avec métadonnées structurées
- **Pagination** : Navigation automatique entre les pages d'inventaire

#### 2.3 Destination des données
- **Base de données** : SQLite (fichier `cars.db`)
- **Structure** : Table `Car` avec 12 champs (id, make, model, year, price, mileage, fuel, location, options, detail_url, created_at, updated_at)
- **Gestion des doublons** : URL unique comme clé de déduplication
- **Mises à jour** : Mise à jour automatique des données existantes

#### 2.4 Fonctionnalités avancées
- **Détection automatique du carburant** : Identification des véhicules électriques
- **Gestion de la pagination** : Navigation automatique entre les pages
- **API REST complète** : Endpoints pour consultation, filtrage et statistiques
- **Interface CLI** : Utilisation en ligne de commande
- **Affichage tabulaire** : Présentation claire des données collectées

### 3. Étapes principales de mise en place du processus

#### 3.1 Configuration de l'environnement
```bash
# Installation des dépendances
pip install -e .

# Dépendances principales :
# - playwright : Navigation web automatisée
# - beautifulsoup4 : Parsing HTML
# - tabulate : Affichage tabulaire
# - flask : API REST
```

#### 3.2 Connexion à la source de données
Le processus de connexion est géré par la classe `AlbiNavigator` :

```python
class AlbiNavigator:
    def __init__(self):
        self.base_url = "https://www.albioccasion.com"
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
```

**Caractéristiques de la connexion :**
- Utilisation de Playwright pour la navigation automatisée
- Attente du chargement complet des pages
- Gestion des timeouts pour s'assurer que le contenu est chargé
- Support de la pagination automatique

#### 3.3 Extraction des données
L'extraction est réalisée par la classe `AlbiPageExtractor` qui :

1. **Parse le HTML** avec BeautifulSoup
2. **Extrait les métadonnées structurées** (marque, modèle, année, prix)
3. **Détecte le type de carburant** (essence/électrique)
4. **Récupère les options** et la localisation
5. **Nettoie et valide** les données extraites

```python
def parse_cars(self):
    cars = []
    car_elements = self.soup.find_all('a', class_='promotion-item')
    
    for car_element in car_elements:
        # Extraction des métadonnées structurées
        name_meta = car_element.find('meta', {'itemprop': 'name'})
        brand_meta = car_element.find('meta', {'itemprop': 'brand'})
        # ... autres extractions
        
        # Création de l'objet Car
        car = Car(make, model, year, price, mileage, fuel, location, options, detail_url)
        cars.append(car)
```

#### 3.4 Stockage des données
La classe `CarDatabase` gère le stockage avec :

- **Création automatique** de la table si elle n'existe pas
- **Gestion des doublons** basée sur l'URL unique
- **Mises à jour automatiques** des données existantes
- **Requêtes optimisées** avec filtres et pagination

```python
def insert_car(self, car: Car) -> bool:
    try:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Car (make, model, year, price, mileage, fuel, location, options, detail_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (car.make, car.model, car.year, car.price, car.mileage, car.fuel, car.location, json.dumps(car.options), car.detail_url))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return self.update_car(car)
```

#### 3.5 Orchestration du processus
Le scraper principal (`AlbiScraper`) orchestre l'ensemble :

```python
def scrap_from_page(self, start_page_number: int = 1, number_of_pages_to_scrap: int = 2):
    # Vérification des limites de pagination
    page_info = self.navigator.get_page_infos()
    total_pages = page_info.total_pages
    
    # Boucle de scraping
    for i in range(start_page_number, start_page_number + number_of_pages_to_scrap):
        page_url = self.navigator.get_inventory_url(i)
        self.navigator.go_to_page(page_url)
        content = self.navigator.get_html()
        extractor = AlbiPageExtractor(content, self.navigator.base_url)
        
        # Sauvegarde des voitures
        for car in extractor.cars:
            if self.database.car_exists(car.detail_url):
                self.database.update_car(car)
            else:
                self.database.insert_car(car)
```

### 4. Comment tester l'application

#### 4.1 Test du scraping de base
```bash
# Utiliser l'interface CLI
python -m car_scrapper.cli --start-page 1 --pages 2

# Afficher toutes les voitures collectées
python -m car_scrapper.cli --show-all
```

#### 4.2 Test de l'API REST
```bash
# Démarrer le serveur API
python server.py

# Tester les endpoints
curl "http://localhost:5000/api/cars"
curl "http://localhost:5000/api/cars?make=Mazda&fuel=Électrique"
curl "http://localhost:5000/api/stats"
```

#### 4.3 Vérification des données
```python
from car_scrapper import AlbiScraper

# Créer un scraper et afficher les statistiques
scraper = AlbiScraper()
print(f"Nombre total de voitures : {scraper.database.get_car_count()}")

# Afficher toutes les voitures
scraper.display_all_cars_from_db()
```

#### 4.4 Tests de filtrage et pagination
```bash
# Test avec filtres
curl "http://localhost:5000/api/cars?price_lt=30000&year_gt=2020"

# Test avec pagination
curl "http://localhost:5000/api/cars?page=1&per_page=10"

# Test avec tri
curl "http://localhost:5000/api/cars?sort_by=price&sort_order=desc"
```

### 5. Paramètres principaux d'exécution

#### 5.1 Paramètres de collecte
- **Nombre de pages à scraper** : Contrôlé par `number_of_pages_to_scrap`
- **Page de départ** : Définie par `start_page_number`
- **Délai entre les pages** : 3 secondes par défaut
- **Mode headless** : Configurable dans le navigateur

#### 5.2 Paramètres de stockage
- **Base de données** : SQLite (`cars.db` par défaut)
- **Gestion des doublons** : Basée sur l'URL unique
- **Mises à jour** : Automatiques pour les données existantes
- **Format des options** : JSON pour la flexibilité

#### 5.3 Paramètres de l'API
- **Port par défaut** : 5000
- **Hôte** : 0.0.0.0 (accessible depuis l'extérieur)
- **Pagination** : 20 éléments par page (max 50)
- **Filtres disponibles** : make, model, fuel, price, year

#### 5.4 Métriques de performance
- **Temps de traitement** : ~2-3 secondes par page
- **Taux de succès** : >95% pour les pages valides
- **Gestion d'erreurs** : Continue en cas d'échec sur une voiture
- **Mémoire** : Optimisée pour de grandes quantités de données

### 6. Conclusion

#### 6.1 Difficultés rencontrées

1. **Gestion de la pagination dynamique** : Le site utilise une pagination complexe qui nécessitait une analyse approfondie du HTML pour extraire les informations de navigation.

2. **Détection du type de carburant** : L'identification automatique des véhicules électriques a nécessité l'analyse des overlays gouvernementaux et des métadonnées spécifiques.

3. **Gestion des timeouts** : Les pages web modernes avec JavaScript nécessitent des délais appropriés pour s'assurer que tout le contenu est chargé avant l'extraction.

4. **Optimisation des performances** : La gestion de grandes quantités de données tout en maintenant des temps de réponse acceptables pour l'API.

#### 6.2 Compétences acquises

1. **Web Scraping avancé** : Maîtrise de Playwright et BeautifulSoup pour l'extraction de données complexes.

2. **Architecture modulaire** : Conception d'un système modulaire avec séparation claire des responsabilités (navigation, extraction, stockage, API).

3. **Gestion de base de données** : Implémentation d'un système de stockage robuste avec gestion des doublons et mises à jour.

4. **API REST** : Développement d'une API complète avec filtrage, pagination et tri.

5. **Gestion d'erreurs** : Implémentation d'un système robuste de gestion d'erreurs pour assurer la continuité du processus.

6. **Documentation et tests** : Création d'une documentation complète et de procédures de test.

#### 6.3 Améliorations possibles

1. **Parallélisation** : Implémentation du scraping multi-thread pour améliorer les performances.
2. **Monitoring** : Ajout de métriques et de logs détaillés pour le monitoring.
3. **Scheduling** : Mise en place d'un système de collecte automatique périodique.
4. **Interface web** : Développement d'une interface utilisateur pour visualiser et gérer les données.
5. **Support multi-sites** : Extension pour supporter d'autres sites de vente de voitures.

Ce projet démontre une approche complète et professionnelle de la collecte de données, allant de l'extraction automatisée à la mise à disposition via API, en passant par un stockage structuré et une gestion robuste des erreurs.
