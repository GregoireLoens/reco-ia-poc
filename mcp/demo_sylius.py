#!/usr/bin/env python3
"""
Démonstration des outils Sylius du serveur MCP
"""
import requests
import json
import time

BASE_URL = "http://localhost:8001"

def demo_sylius_tools():
    """Démontre l'utilisation des outils Sylius"""
    print("🛍️  Démonstration des outils Sylius MCP")
    print("=" * 50)

    # Attendre que le serveur soit prêt
    print("⏳ Attente du serveur MCP...")
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                break
        except:
            pass
        time.sleep(2)
        print(f"   Tentative {i+1}/30...")

    print("✅ Serveur MCP prêt!")

    print("\n📋 Liste des outils disponibles:")
    try:
        response = requests.get(f"{BASE_URL}/tools")
        tools = response.json()["tools"]
        for tool in tools:
            print(f"   • {tool['name']}: {tool['description']}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    print("\n🛒 1. Récupération des produits Sylius:")
    try:
        data = {"arguments": {"limit": 3}}
        response = requests.post(f"{BASE_URL}/tools/get_sylius_products", json=data)
        products = response.json()["result"]
        print(f"   ✅ {len(products)} produits trouvés:")
        for product in products:
            print(f"      - {product['code']}: {product['name']} ({len(product['variants'])} variant(s))")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n🔍 2. Recherche d'un produit par code:")
    try:
        data = {"arguments": {"code": "TSHIRT_RED"}}
        response = requests.post(f"{BASE_URL}/tools/get_sylius_product_by_code", json=data)
        product = response.json()["result"]
        if product:
            print(f"   ✅ Produit trouvé: {product['name']}")
            print(f"      Code: {product['code']}")
            print(f"      Description: {product['description']}")
            print(f"      Variants: {len(product['variants'])}")
        else:
            print("   ❌ Produit non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n🔎 3. Recherche par nom/description:")
    try:
        data = {"arguments": {"query": "t-shirt", "limit": 5}}
        response = requests.post(f"{BASE_URL}/tools/search_sylius_products", json=data)
        products = response.json()["result"]
        print(f"   ✅ {len(products)} produit(s) trouvé(s) pour 't-shirt':")
        for product in products:
            print(f"      - {product['code']}: {product['name']}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n🎯 4. Test via interface MCP (JSON-RPC):")
    try:
        mcp_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_sylius_products",
                "arguments": {"limit": 2}
            }
        }
        response = requests.post(f"{BASE_URL}/mcp", json=mcp_data)
        result = response.json()
        if "result" in result:
            content = result["result"]["content"][0]["text"]
            print("   ✅ Interface MCP fonctionnelle")
            print(f"      Résultat: {content[:100]}...")
        else:
            print("   ❌ Erreur MCP")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n" + "=" * 50)
    print("🎉 Démonstration terminée!")
    print("\n💡 Vous pouvez maintenant utiliser ces outils pour:")
    print("   • Intégrer Sylius avec des assistants IA")
    print("   • Créer des chatbots e-commerce")
    print("   • Automatiser des tâches liées aux produits")
    print("   • Développer des applications tierces")

if __name__ == "__main__":
    demo_sylius_tools()