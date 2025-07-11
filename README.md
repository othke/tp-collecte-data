# Car Scrapper

Un outil de scraping pour les sites de vente de voitures, spécialement conçu pour Albi.ca.

Présentation du projet : [Presentation](https://othke.github.io/tp-collecte-data/)

## 🚀 Installation

### Installation en mode développement
```bash
# Cloner le repository
git clone <repository-url>
cd car_scrapper

# Installer en mode développement
pip install -e .
```

### Installation directe
```bash
pip install .
```

## 📦 Structure du projet

```
car_scrapper/
├── car_scrapper/
│   ├── __init__.py          # Point d'entrée du paquet
│   ├── models.py            # Classes de données (Car, PageInfo)
│   ├── database.py          # Gestionnaire de base de données SQLite
│   ├── extractor.py         # Extracteur de données HTML
│   ├── navigator.py         # Navigateur web avec Playwright
│   ├── scraper.py           # Scraper principal
│   └── cli.py              # Interface en ligne de commande
├── main.py                  # Script principal
├── setup.py                 # Configuration du paquet
├── requirements.txt         # Dépendances
└── README.md               # Documentation
```

## 🛠️ Utilisation

### Utilisation simple
```python
from car_scrapper import AlbiScraper

# Créer un scraper
scraper = AlbiScraper()

# Scraper 2 pages à partir de la page 1
scraper.scrap_from_page(1, 2)

# Afficher toutes les voitures de la base de données
scraper.display_all_cars_from_db()
```

### Utilisation en ligne de commande
```bash
# Scraper 1 page
python -m car_scrapper.cli

# Scraper 3 pages à partir de la page 2
python -m car_scrapper.cli --start-page 2 --pages 3

# Afficher toutes les voitures de la base de données
python -m car_scrapper.cli --show-all

# Utiliser une base de données personnalisée
python -m car_scrapper.cli --db-path my_cars.db
```

### Utilisation comme script
```bash
# Exécuter le script principal
python main.py
```

### 🚀 API REST

Le projet inclut une API REST pour accéder aux données via HTTP.

#### Démarrer le serveur API
```bash
# Serveur par défaut (port 5000)
python server.py

# Serveur personnalisé
python server.py --host 127.0.0.1 --port 8080 --debug

# Avec base de données personnalisée
python server.py --db-path my_cars.db
```

#### Endpoints disponibles

**GET /api/cars** - Liste des voitures avec filtres et pagination
```bash
# Toutes les voitures
curl "http://localhost:5000/api/cars"

# Avec pagination
curl "http://localhost:5000/api/cars?page=1&per_page=10"

# Avec filtres
curl "http://localhost:5000/api/cars?make=Mazda&fuel=Électrique&price_lt=30000"

# Avec tri
curl "http://localhost:5000/api/cars?sort_by=price&sort_order=desc"
```

**GET /api/cars/{id}** - Détails d'une voiture
```bash
curl "http://localhost:5000/api/cars/1"
```

**GET /api/stats** - Statistiques de la base de données
```bash
curl "http://localhost:5000/api/stats"
```

#### Paramètres de filtrage
- `make` : Marque du véhicule
- `model` : Modèle du véhicule
- `fuel` : Type de carburant (Essence/Électrique)
- `price_lt` : Prix inférieur à
- `price_gt` : Prix supérieur à
- `year_lt` : Année inférieure à
- `year_gt` : Année supérieure à

#### Paramètres de pagination
- `page` : Numéro de page (défaut: 1)
- `per_page` : Nombre d'éléments par page (max: 50, défaut: 20)

#### Paramètres de tri
- `sort_by` : Champ de tri (id, make, model, year, price, mileage, fuel, location)
- `sort_order` : Ordre de tri (asc, desc)

## 🗄️ Base de données

Le scraper utilise SQLite pour stocker les données des voitures. Chaque voiture est identifiée par son `detail_url` unique.

### Structure de la table `Car` :
- `id` : Identifiant unique
- `make` : Marque du véhicule
- `model` : Modèle du véhicule
- `year` : Année du véhicule
- `price` : Prix en dollars
- `mileage` : Kilométrage
- `fuel` : Type de carburant (Essence/Électrique)
- `location` : Localisation du véhicule
- `options` : Options du véhicule (JSON)
- `detail_url` : URL de détail (unique)
- `created_at` : Date de création
- `updated_at` : Date de mise à jour

## 🔧 Fonctionnalités

- ✅ **Scraping automatique** : Extraction des données de voitures
- ✅ **Détection de carburant** : Identification automatique des véhicules électriques
- ✅ **Base de données SQLite** : Stockage persistant des données
- ✅ **Gestion des doublons** : Mise à jour automatique des données existantes
- ✅ **Interface CLI** : Utilisation en ligne de commande
- ✅ **Affichage tabulaire** : Présentation claire des données avec tabulate
- ✅ **Navigation paginée** : Gestion automatique de la pagination

## 📋 Dépendances

- `playwright` : Navigation web automatisée
- `beautifulsoup4` : Parsing HTML
- `tabulate` : Affichage tabulaire
- `sqlite3` : Base de données (inclus avec Python)
