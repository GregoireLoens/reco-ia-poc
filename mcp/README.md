# MCP Server avec intégration Sylius

Un serveur MCP (Model Context Protocol) qui expose les fonctionnalités de base et l'accès aux produits Sylius.

## Fonctionnalités

### Outils de base
- `hello_world(name: str)` : Retourne un message de salutation
- `get_current_time()` : Retourne l'heure actuelle

### Outils Sylius
- `get_sylius_products(limit: int, offset: int)` : Récupère la liste des produits Sylius
- `get_sylius_product_by_code(code: str)` : Récupère un produit spécifique par son code
- `search_sylius_products(query: str, limit: int)` : Recherche des produits par nom ou description

## Lancement avec Docker

Le serveur MCP est maintenant intégré avec Sylius et utilise le même réseau Docker.

### Avec le Makefile (recommandé)

```bash
# À la racine du projet
make all-up          # Lance Sylius + MCP
make all-down        # Arrête tout
make status          # Vérifie le statut
make logs           # Voit les logs
```

### Manuellement

```bash
# Terminal 1: Sylius
cd shop && docker-compose up -d

# Terminal 2: MCP
cd mcp && docker-compose up -d
```

Le serveur MCP sera accessible sur `http://localhost:8001` et se connecte automatiquement à la base de données Sylius.

### Endpoints

- `GET /` : Page d'accueil
- `GET /health` : Vérification de santé
- `GET /tools` : Liste des outils disponibles
- `POST /tools/{tool_name}` : Appel d'un outil spécifique
- `POST /mcp` : Interface MCP complète (JSON-RPC 2.0)

### Exemples d'utilisation

#### Via HTTP direct

```bash
# Tester la connexion
curl http://localhost:8001/

# Lister les outils
curl http://localhost:8001/tools

# Appeler hello_world
curl -X POST http://localhost:8001/tools/hello_world \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"name": "Alice"}}'

# Obtenir l'heure actuelle
curl -X POST http://localhost:8001/tools/get_current_time \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Via MCP (JSON-RPC 2.0)

```bash
# Lister les outils
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list"
  }'

# Appeler un outil
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "hello_world",
      "arguments": {"name": "Bob"}
    }
  }'

# Récupérer les produits Sylius
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "get_sylius_products",
      "arguments": {"limit": 5}
    }
  }'

# Rechercher un produit par code
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "get_sylius_product_by_code",
      "arguments": {"code": "MY_PRODUCT_CODE"}
    }
  }'

# Rechercher des produits par nom
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 5,
    "method": "tools/call",
    "params": {
      "name": "search_sylius_products",
      "arguments": {"query": "t-shirt", "limit": 10}
    }
  }'
```

## Données de test

Le serveur crée automatiquement des données de test Sylius lors du premier démarrage :

- **TSHIRT_RED** : T-Shirt Rouge (19.99€)
- **JEANS_BLUE** : Jean Bleu (49.99€)
- **SHOES_BLACK** : Chaussures Noires (79.99€)
- **HAT_GREEN** : Chapeau Vert (14.99€)
- **BAG_BROWN** : Sac Marron (39.99€)

Chaque produit a :
- Un variant par défaut
- Un stock de 100 unités
- Des traductions en anglais

## Développement local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
python server.py
```

## Structure du projet

```
mcp/
├── server.py          # Serveur MCP principal
├── test_server.py    # Script de test
├── requirements.txt   # Dépendances Python
├── Dockerfile         # Configuration Docker
├── docker-compose.yml # Configuration Docker Compose
└── README.md          # Documentation
```

## Architecture

Le serveur MCP se compose de :

- **Serveur FastAPI** : API REST pour les appels d'outils
- **Modèles SQLAlchemy** : Mapping des entités Sylius (Product, ProductVariant, etc.)
- **Connexion MySQL** : Accès à la base de données Sylius
- **Interface MCP** : Protocole JSON-RPC 2.0 pour l'intégration

## Configuration de la base de données

Le serveur se connecte automatiquement à la base de données MySQL de Sylius :

- **Host** : mysql (dans le réseau Docker)
- **Port** : 3306
- **Database** : sylius
- **User** : root (sans mot de passe)

Pour utiliser une base de données différente, modifiez la variable `DATABASE_URL` dans `models.py`.

## Test du serveur

Un script de test complet est fourni :

```bash
python test_server.py
```

## Démonstration Sylius

Pour voir les outils Sylius en action :

```bash
python demo_sylius.py
```

Ce script démontre :
- Récupération des produits
- Recherche par code
- Recherche par nom/description
- Utilisation de l'interface MCP