#!/bin/bash
# Script de démarrage pour le serveur MCP avec Sylius

echo "🚀 Démarrage du serveur MCP Sylius..."

# Attendre que MySQL (de Sylius) soit prêt
echo "⏳ Attente de MySQL..."
while ! mysqladmin ping -h mysql -P 3306 --silent; do
    echo "   MySQL n'est pas encore prêt..."
    sleep 2
done

echo "✅ MySQL est prêt!"

# Le serveur MCP utilise maintenant la base Sylius existante
# Plus besoin d'initialiser de données de test

# Lancer le serveur MCP
echo "🎯 Lancement du serveur MCP..."
python server.py