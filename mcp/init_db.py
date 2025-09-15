#!/usr/bin/env python3
"""
Script d'initialisation de la base de données Sylius avec des données de test
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import engine, Base, Product, ProductVariant, ProductTranslation, ProductVariantTranslation
from sqlalchemy.orm import sessionmaker
from datetime import datetime

def init_database():
    """Initialise la base de données avec des données de test"""
    print("🔧 Initialisation de la base de données Sylius...")

    # Créer les tables
    Base.metadata.create_all(bind=engine)

    # Créer une session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Vérifier si des données existent déjà
        existing_products = db.query(Product).count()
        if existing_products > 0:
            print(f"✅ La base de données contient déjà {existing_products} produits")
            return

        print("📝 Création de données de test...")

        # Créer des produits de test
        products_data = [
            {
                "code": "TSHIRT_RED",
                "name": "T-Shirt Rouge",
                "description": "Un beau t-shirt rouge de qualité supérieure",
                "price": 19.99
            },
            {
                "code": "JEANS_BLUE",
                "name": "Jean Bleu",
                "description": "Jean bleu classique pour toutes occasions",
                "price": 49.99
            },
            {
                "code": "SHOES_BLACK",
                "name": "Chaussures Noires",
                "description": "Chaussures élégantes en cuir véritable",
                "price": 79.99
            },
            {
                "code": "HAT_GREEN",
                "name": "Chapeau Vert",
                "description": "Chapeau vert stylé pour compléter votre look",
                "price": 14.99
            },
            {
                "code": "BAG_BROWN",
                "name": "Sac Marron",
                "description": "Sac en cuir marron spacieux et durable",
                "price": 39.99
            }
        ]

        for product_data in products_data:
            # Créer le produit
            product = Product(
                code=product_data["code"],
                enabled=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(product)
            db.flush()  # Pour obtenir l'ID

            # Créer la traduction
            translation = ProductTranslation(
                product_id=product.id,
                name=product_data["name"],
                description=product_data["description"],
                locale="en_US"
            )
            db.add(translation)

            # Créer le variant
            variant = ProductVariant(
                product_id=product.id,
                code=f"{product_data['code']}_DEFAULT",
                position=0,
                enabled=True,
                tracked=True,
                on_hand=100,
                on_hold=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(variant)
            db.flush()

            # Créer la traduction du variant
            variant_translation = ProductVariantTranslation(
                variant_id=variant.id,
                name=product_data["name"],
                locale="en_US"
            )
            db.add(variant_translation)

        # Commit des changements
        db.commit()

        print(f"✅ {len(products_data)} produits de test créés avec succès!")
        print("\n📋 Produits créés:")
        for product_data in products_data:
            print(f"   - {product_data['code']}: {product_data['name']} ({product_data['price']}€)")

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()