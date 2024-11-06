from app import db

class Category(db.Model):
    __tablename__ = 'Category'
    
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)
