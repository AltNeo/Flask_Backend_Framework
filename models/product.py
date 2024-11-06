from app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'Product'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    descr = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'))
    estimated_price = db.Column(db.Float)
    material = db.Column(db.String(100))
    margin = db.Column(db.Float)
    displaystate = db.Column(db.Boolean, default=True)
    images = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
