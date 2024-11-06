from app import db
from datetime import datetime

class Enquiry(db.Model):
    __tablename__ = 'Enquiry'
    
    enquiry_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    response = db.Column(db.Text)
    response_date = db.Column(db.DateTime)
    design_upload = db.Column(db.Text)
    enquiry_text = db.Column(db.Text)
    enquiry_quantity = db.Column(db.Integer)
    enquiry_status = db.Column(db.String(20), default='pending')
    enquiry_quote = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.product_id'))
