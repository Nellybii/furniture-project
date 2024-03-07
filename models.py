from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# from sqlalchemy.orm import validates

db=SQLAlchemy()
bcrypt=Bcrypt()

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String)
    role=db.Column(db.String, server_default='member')
    password = db.Column(db.String)
    created_at=db.Column(db.TIMESTAMP, default=db.func.now())
    updated_at=db.Column(db.TIMESTAMP,onupdate=db.func.now())
    products=db.relationship("ProductModel", backref="users",lazy=True) 
    reviews=db.relationship("ReviewModel", backref="users", lazy=True)
    orders=db.relationship("OrderModel",backref="users",lazy=True)
 
    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.password, plain_password)

    def to_json(self):
        return {
            'id': self.id,
            'role': self.role,
        }
    
class ProductModel (db.Model):
    __tablename__="products"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    title=db.Column(db.String(80),nullable=False)
    description=db.Column(db.Text,nullable=False)
    price=db.Column(db.Float,nullable=False)
    image_url=db.Column(db.String, nullable=False)
    reviews=db.relationship("ReviewModel",backref="products",lazy=True)
    category_id=db.Column(db.Integer,db.ForeignKey("categories.id"),nullable=False)
    # orders=db.relationship("OrderModel",backref="products",lazy=True)
    orders=db.relationship("OrderModel",backref="products",lazy=True,cascade="all, delete-orphan",)
   
    
class CategoryModel(db.Model):
    __tablename__="categories"   
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    image_url=db.Column(db.String, nullable=False)
    products=db.relationship("ProductModel",backref="categories",lazy=True)


class ReviewModel(db.Model):
    __tablename__="reviews"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=True)
    product_id=db.Column(db.Integer,db.ForeignKey("products.id"),nullable=True)
    text=db.Column(db.Text,nullable=False)
    rating=db.Column(db.Integer,nullable=False)
    
class OrderModel(db.Model):
    __tablename__="orders"
    id=db.Column(db.Integer,primary_key=True)  
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False) 
    product_id=db.Column(db.Integer,db.ForeignKey("products.id"),nullable=False) 
    total_price=db.Column(db.Float,nullable=False)
    status=db.Column(db.String,nullable=False)
    order_at=db.Column(db.TIMESTAMP(),default=db.func.now())

    # invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'))

class InvoiceModel(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False, default=db.func.now())
    total_amount = db.Column(db.Float, nullable=False)
   
    order = db.relationship('OrderModel', backref='invoice', uselist=False)


#     payment = db.relationship('PaymentModel', backref='orders')
    
# class PaymentModel(db.Model):
#     __tablename__ = 'payments'
#     id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Float)
#     payment_type = db.Column(db.String(50), nullable=False)
#     status = db.Column(db.String(50), nullable=False)
#     payment_date = db.Column(db.DateTime, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    

