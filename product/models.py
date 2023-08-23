from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from core.database import Base


class Products(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    name = Column(String(50))
    category_id = Column(ForeignKey("product_categories.id"))
    skus = relationship("ProductSkus", backref="product")


class ProductCategories(Base):
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    name = Column(String(50))
    products = relationship("Products", backref="category")


class ProductSkus(Base):
    __tablename__ = "product_skus"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    price = Column(Integer)
    quantity = Column(Integer) 
    image = Column(String(255))
    product_id = Column(ForeignKey("products.id"))
    attributes = relationship("Attributes", secondary='product_attribute')


class Attributes(Base):
    __tablename__ = "attributes"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    value = Column(String(50))
    skus = relationship(ProductSkus, secondary='product_attribute')


class ProductAttributes(Base):
    __tablename__ = "product_attribute"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    skus_id = Column(Integer, ForeignKey(ProductSkus.id))
    attribute_id = Column(Integer, ForeignKey(Attributes.id))
