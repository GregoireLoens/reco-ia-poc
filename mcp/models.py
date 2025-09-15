"""
Modèles de base de données pour Sylius
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'sylius_product'

    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    enabled = Column(Boolean, default=True)

    # Relations
    translations = relationship("ProductTranslation", back_populates="product")
    variants = relationship("ProductVariant", back_populates="product")

    def get_name(self, locale='en_US'):
        """Retourne le nom du produit dans la locale spécifiée"""
        for translation in self.translations:
            if translation.locale == locale:
                return translation.name
        # Retourne le premier nom disponible si la locale n'est pas trouvée
        return self.translations[0].name if self.translations else self.code

    def get_description(self, locale='en_US'):
        """Retourne la description du produit dans la locale spécifiée"""
        for translation in self.translations:
            if translation.locale == locale:
                return translation.description
        return self.translations[0].description if self.translations else ""

class ProductTranslation(Base):
    __tablename__ = 'sylius_product_translation'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    locale = Column(String(10), nullable=False)
    product_id = Column(Integer, ForeignKey('sylius_product.id'))

    product = relationship("Product", back_populates="translations")

class ProductVariant(Base):
    __tablename__ = 'sylius_product_variant'

    id = Column(Integer, primary_key=True)
    code = Column(String(255), unique=True, nullable=False)
    position = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    enabled = Column(Boolean, default=True)
    tracked = Column(Boolean, default=False)
    on_hold = Column(Integer, default=0)
    on_hand = Column(Integer, default=0)
    weight = Column(Float)
    width = Column(Float)
    height = Column(Float)
    depth = Column(Float)
    product_id = Column(Integer, ForeignKey('sylius_product.id'))

    # Relations
    product = relationship("Product", back_populates="variants")
    translations = relationship("ProductVariantTranslation", back_populates="variant")

    def get_price(self):
        """Retourne le prix du variant (simplifié)"""
        # Dans Sylius, les prix sont plus complexes, mais pour cet exemple on retourne une valeur fixe
        return 29.99

class ProductVariantTranslation(Base):
    __tablename__ = 'sylius_product_variant_translation'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    locale = Column(String(10), nullable=False)
    variant_id = Column(Integer, ForeignKey('sylius_product_variant.id'))

    variant = relationship("ProductVariant", back_populates="translations")

# Configuration de la base de données
DATABASE_URL = "mysql+pymysql://root:@mysql:3306/sylius"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Retourne une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()