from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'OrderHistory'
    
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customer.customer_id'))
    shipping_address = db.Column(db.Text)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    contact_number = db.Column(db.String(20))
    payment_id = db.Column(db.String(100))
    enquiry_id = db.Column(db.Integer, db.ForeignKey('Enquiry.enquiry_id'))
