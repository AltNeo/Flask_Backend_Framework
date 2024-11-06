from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'Customer'
    
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text)
    pin = db.Column(db.String(10))
    otp_timestamp = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
