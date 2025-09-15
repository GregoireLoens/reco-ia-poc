# MCP Hello World Server

Un serveur MCP (Model Context Protocol) simple en Python qui fournit des fonctionnalités de base.

## Fonctionnalités

- `hello_world(name: str)` : Retourne un message de salutation
- `get_current_time()` : Retourne l'heure actuelle

## Lancement avec Docker

```bash
# Construire et lancer le serveur
docker-compose up --build

# Ou en arrière-plan
docker-compose up --build -d

# Arrêter le serveur
docker-compose down
```

## Utilisation

Le serveur sera accessible sur `http://localhost:8001`

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
```

## Test du serveur

Un script de test est fourni pour vérifier toutes les fonctionnalités :

```bash
python test_server.py
```

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

## Technologies utilisées

- **Python 3.11** : Langage de programmation
- **FastAPI** : Framework web pour l'API REST
- **Uvicorn** : Serveur ASGI
- **Pydantic** : Validation des données
- **Docker** : Containerisation