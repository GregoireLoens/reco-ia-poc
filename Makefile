.PHONY: help up down restarsylius-install: ## Installe Sylius avec des données d'exemple
	@echo "🔧 Installation de Sylius..."
	./install_sylius.shogs clean sylius-up sylius-down mcp-up mcp-down all-up all-down

# Variables
SYLIUS_DIR = shop
MCP_DIR = mcp
NETWORK_NAME = reco-ia-network

help: ## Affiche cette aide
	@echo "Commandes disponibles pour gérer Sylius et MCP :"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Commandes pour Sylius uniquement
sylius-up: ## Lance uniquement Sylius
	@echo "🚀 Lancement de Sylius..."
	cd $(SYLIUS_DIR) && docker-compose up -d
	@echo "⏳ Attente que Sylius soit prêt..."
	@sleep 10
	@echo "✅ Sylius est accessible sur http://localhost"

sylius-down: ## Arrête Sylius
	@echo "🛑 Arrêt de Sylius..."
	cd $(SYLIUS_DIR) && docker-compose down

sylius-logs: ## Affiche les logs de Sylius
	cd $(SYLIUS_DIR) && docker-compose logs -f

sylius-install: ## Installe Sylius avec des données d'exemple
	@echo "� Installation de Sylius..."
	./install_sylius.sh

# Commandes pour MCP uniquement
mcp-up: ## Lance uniquement le serveur MCP
	@echo "🚀 Lancement du serveur MCP..."
	cd $(MCP_DIR) && docker-compose up -d
	@echo "⏳ Attente que MCP soit prêt..."
	@sleep 15
	@echo "✅ MCP est accessible sur http://localhost:8001"

mcp-down: ## Arrête le serveur MCP
	@echo "🛑 Arrêt du serveur MCP..."
	cd $(MCP_DIR) && docker-compose down

mcp-logs: ## Affiche les logs du serveur MCP
	cd $(MCP_DIR) && docker-compose logs -f

mcp-restart: ## Redémarre le serveur MCP
	@echo "🔄 Redémarrage du serveur MCP..."
	cd $(MCP_DIR) && docker-compose restart

mcp-test: ## Teste le serveur MCP
	@echo "🧪 Test du serveur MCP..."
	cd $(MCP_DIR) && python3 test_server.py

mcp-demo: ## Lance la démonstration Sylius du MCP
	@echo "🛍️  Démonstration des outils Sylius..."
	cd $(MCP_DIR) && python3 demo_sylius.py

# Commandes pour les deux services ensemble
all-up: network-create ## Lance Sylius et MCP ensemble
	@echo "🚀 Lancement de Sylius et MCP..."
	$(MAKE) sylius-up
	$(MAKE) mcp-up
	@echo ""
	@echo "🎉 Services démarrés !"
	@echo "   📊 Sylius : http://localhost"
	@echo "   🤖 MCP    : http://localhost:8001"
	@echo ""
	@echo "Commandes utiles :"
	@echo "   make logs          # Voir tous les logs"
	@echo "   make mcp-test      # Tester MCP"
	@echo "   make mcp-demo      # Démonstration Sylius"

all-down: ## Arrête Sylius et MCP
	@echo "🛑 Arrêt de Sylius et MCP..."
	$(MAKE) mcp-down
	$(MAKE) sylius-down
	$(MAKE) network-remove

all-restart: ## Redémarre Sylius et MCP
	@echo "🔄 Redémarrage de Sylius et MCP..."
	$(MAKE) all-down
	$(MAKE) all-up

# Gestion du réseau
network-create: ## Crée le réseau partagé
	@echo "🌐 Création du réseau $(NETWORK_NAME)..."
	@docker network create $(NETWORK_NAME) 2>/dev/null || echo "Réseau $(NETWORK_NAME) existe déjà"

network-remove: ## Supprime le réseau partagé
	@echo "🗑️  Suppression du réseau $(NETWORK_NAME)..."
	@docker network rm $(NETWORK_NAME) 2>/dev/null || echo "Réseau $(NETWORK_NAME) n'existe pas"

# Logs et monitoring
logs: ## Affiche les logs de tous les services
	@echo "📋 Logs Sylius (Ctrl+C pour quitter) :"
	@echo "======================================"
	@cd $(SYLIUS_DIR) && docker-compose logs -f --tail=50 &
	@echo ""
	@echo "📋 Logs MCP (dans un autre terminal) :"
	@echo "======================================"
	@echo "make mcp-logs"

status: ## Affiche le statut de tous les services
	@echo "📊 Statut des services :"
	@echo "========================"
	@echo "Sylius :"
	@cd $(SYLIUS_DIR) && docker-compose ps
	@echo ""
	@echo "MCP :"
	@cd $(MCP_DIR) && docker-compose ps

# Nettoyage
clean: all-down ## Nettoie tous les conteneurs et volumes
	@echo "🧹 Nettoyage complet..."
	docker system prune -f
	docker volume prune -f

# Commandes d'alias
up: all-up ## Alias pour all-up
down: all-down ## Alias pour all-down
restart: all-restart ## Alias pour all-restart

# Commandes de développement
dev-setup: ## Configuration initiale pour le développement
	@echo "🔧 Configuration du développement..."
	$(MAKE) network-create
	@echo "✅ Réseau créé"
	@echo "💡 Utilisez 'make all-up' pour démarrer tous les services"

dev-clean: clean ## Nettoyage complet pour le développement
	@echo "🧹 Nettoyage complet du développement terminé"