from flask_sqlalchemy import SQLAlchemy
from app import db

# Import all models here
from .product import Product
from .category import Category
from .customer import Customer
from .order import Order
from .enquiry import Enquiry
