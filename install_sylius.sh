#!/bin/bash
# Script d'installation de Sylius avec données d'exemple

echo "🔧 Installation de Sylius avec données d'exemple..."

# Attendre que Sylius soit complètement prêt
echo "⏳ Attente que Sylius soit prêt..."
sleep 10

# Installer Sylius
echo "📦 Installation de Sylius..."
cd shop
docker-compose exec -T php bash -c "
    composer install --no-interaction
    php bin/console doctrine:database:create --if-not-exists --no-interaction
    php bin/console doctrine:migrations:migrate --no-interaction
    php bin/console sylius:fixtures:load --no-interaction
"

echo "✅ Sylius installé avec données d'exemple!"
echo ""
echo "🎉 Installation terminée!"
echo "   📊 Sylius Shop : http://localhost"
echo "   👨‍💼 Sylius Admin : http://localhost/admin"
echo "   🤖 MCP Server : http://localhost:8001"
echo ""
echo "Comptes de test :"
echo "   Admin : sylius@example.com / sylius"
echo "   Client : shop@example.com / sylius"