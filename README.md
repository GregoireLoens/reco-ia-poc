# Reco IA POC - Sylius + MCP Server

Ce projet contient une plateforme e-commerce Sylius complète avec un serveur MCP (Model Context Protocol) pour exposer les produits via des APIs.

## Architecture

- **Sylius** : Plateforme e-commerce complète (http://localhost)
- **MCP Server** : Serveur d'API pour accéder aux produits Sylius (http://localhost:8001)
- **MySQL** : Base de données partagée entre Sylius et MCP

## Démarrage rapide

### Première installation

```bash
# 1. Démarrer les services
make all-up

# 2. Installer Sylius avec données d'exemple
make sylius-install

# 3. Tester le MCP
make mcp-demo
```

### Démarrage normal (après installation)

```bash
make all-up
```

Cette commande :
1. Crée le réseau Docker partagé
2. Lance Sylius (boutique + admin)
3. Lance le serveur MCP
4. Configure la connectivité entre les services

### Services accessibles

- **Sylius Shop** : http://localhost
- **Sylius Admin** : http://localhost/admin
- **MCP Server** : http://localhost:8001
- **MailHog** : http://localhost:8025 (emails de test)

## Commandes Makefile

### Gestion complète
```bash
make help           # Affiche toutes les commandes disponibles
make all-up         # Lance tout (Sylius + MCP)
make all-down       # Arrête tout
make all-restart    # Redémarre tout
make status         # Vérifie le statut des services
make logs           # Affiche tous les logs
```

### Sylius uniquement
```bash
make sylius-up      # Lance Sylius
make sylius-down    # Arrête Sylius
make sylius-logs    # Logs Sylius
make sylius-restart # Redémarre Sylius
```

### MCP uniquement
```bash
make mcp-up         # Lance le serveur MCP
make mcp-down       # Arrête MCP
make mcp-logs       # Logs MCP
make mcp-restart    # Redémarre MCP
make mcp-test       # Teste les APIs MCP
make mcp-demo       # Démonstration des outils Sylius
```

### Maintenance
```bash
make clean          # Nettoyage complet
make dev-setup      # Configuration développement
make dev-clean      # Nettoyage développement
```

## Utilisation du MCP Server

Le serveur MCP expose des outils pour interagir avec les produits Sylius :

### Outils disponibles
- `get_sylius_products(limit, offset)` - Liste des produits
- `get_sylius_product_by_code(code)` - Produit par code
- `search_sylius_products(query, limit)` - Recherche par nom

### Exemples d'utilisation

```bash
# Tester la connexion
curl http://localhost:8001/health

# Lister les outils
curl http://localhost:8001/tools

# Récupérer des produits
curl -X POST http://localhost:8001/tools/get_sylius_products \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"limit": 5}}'

# Rechercher un produit
curl -X POST http://localhost:8001/tools/get_sylius_product_by_code \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"code": "YOUR_PRODUCT_CODE"}}'
```

## Comptes de test Sylius

### Administrateur
- **Email** : sylius@example.com
- **Mot de passe** : sylius
- **Accès** : http://localhost/admin

### Client exemple
- **Email** : shop@example.com
- **Mot de passe** : sylius

## Structure du projet

```
├── shop/                 # Application Sylius
│   ├── compose.yml       # Configuration Docker Sylius
│   └── ...               # Code Sylius
├── mcp/                  # Serveur MCP
│   ├── server.py         # Serveur FastAPI
│   ├── models.py         # Modèles de données Sylius
│   ├── docker-compose.yml # Configuration Docker MCP
│   └── ...               # Scripts et tests
├── Makefile             # Commandes de gestion
└── README.md            # Cette documentation
```

## Développement

### Prérequis
- Docker & Docker Compose
- Make (généralement installé avec les build tools)

### Configuration
Le réseau Docker `reco-ia-network` est automatiquement créé et partagé entre tous les services.

### Dépannage

**Problème : Port déjà utilisé**
```bash
# Vérifier les ports utilisés
docker ps
make all-down
make all-up
```

**Problème : Services ne communiquent pas**
```bash
# Recréer le réseau
make network-remove
make network-create
make all-restart
```

**Problème : Base de données inaccessible**
```bash
# Vérifier les logs MySQL
make sylius-logs
```

## Technologies

- **Sylius** : Framework e-commerce PHP/Symfony
- **MCP Server** : Python FastAPI + SQLAlchemy
- **Base de données** : MySQL 8.4
- **Conteneurisation** : Docker & Docker Compose