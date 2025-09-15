#!/usr/bin/env python3
"""
Script de test pour le serveur MCP Hello World
Teste toutes les fonctionnalités du serveur MCP
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8001"

def test_endpoint(url, method="GET", data=None, expected_status=200):
    """Test un endpoint et retourne le résultat"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        else:
            print(f"❌ Méthode HTTP non supportée: {method}")
            return False

        if response.status_code == expected_status:
            print(f"✅ {method} {url} - Status: {response.status_code}")
            return response.json() if response.content else True
        else:
            print(f"❌ {method} {url} - Status: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion pour {url}: {e}")
        return False

def main():
    print("🚀 Test du serveur MCP Hello World")
    print("=" * 50)

    # Test 1: Page d'accueil
    print("\n1. Test de la page d'accueil")
    result = test_endpoint(f"{BASE_URL}/")
    if result:
        print(f"   Message: {result.get('message', 'N/A')}")

    # Test 2: Santé du serveur
    print("\n2. Test de la santé du serveur")
    result = test_endpoint(f"{BASE_URL}/health")
    if result:
        print(f"   Status: {result}")

    # Test 3: Liste des outils
    print("\n3. Test de la liste des outils")
    result = test_endpoint(f"{BASE_URL}/tools")
    if result and isinstance(result, list):
        print(f"   Nombre d'outils: {len(result)}")
        for tool in result:
            print(f"   - {tool.get('name', 'N/A')}: {tool.get('description', 'N/A')}")

    # Test 4: Appel hello_world
    print("\n4. Test de l'outil hello_world")
    data = {"arguments": {"name": "Alice"}}
    result = test_endpoint(f"{BASE_URL}/tools/hello_world", "POST", data)
    if result:
        print(f"   Résultat: {result}")

    # Test 5: Appel get_current_time
    print("\n5. Test de l'outil get_current_time")
    result = test_endpoint(f"{BASE_URL}/tools/get_current_time", "POST", {})
    if result:
        print(f"   Résultat: {result}")

    # Test 6: Interface MCP - tools/list
    print("\n6. Test MCP - Liste des outils")
    mcp_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    result = test_endpoint(f"{BASE_URL}/mcp", "POST", mcp_data)
    if result:
        tools = result.get("result", {}).get("tools", [])
        print(f"   Nombre d'outils MCP: {len(tools)}")
        for tool in tools:
            print(f"   - {tool.get('name', 'N/A')}")

    # Test 7: Interface MCP - tools/call hello_world
    print("\n7. Test MCP - Appel hello_world")
    mcp_data = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "hello_world",
            "arguments": {"name": "Bob"}
        }
    }
    result = test_endpoint(f"{BASE_URL}/mcp", "POST", mcp_data)
    if result:
        content = result.get("result", {}).get("content", [])
        if content:
            print(f"   Résultat: {content[0].get('text', 'N/A')}")

    # Test 8: Interface MCP - tools/call get_current_time
    print("\n8. Test MCP - Appel get_current_time")
    mcp_data = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_current_time",
            "arguments": {}
        }
    }
    result = test_endpoint(f"{BASE_URL}/mcp", "POST", mcp_data)
    if result:
        content = result.get("result", {}).get("content", [])
        if content:
            print(f"   Résultat: {content[0].get('text', 'N/A')}")

    print("\n" + "=" * 50)
    print("🎉 Tests terminés !")
    print("\nPour lancer le serveur:")
    print("  docker-compose up --build")
    print("\nPour tester manuellement:")
    print(f"  curl {BASE_URL}/")
    print(f"  curl {BASE_URL}/tools")

if __name__ == "__main__":
    main()