from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_jwt_extended import jwt_required,  current_user
from models import db, ProductModel
import logging

# Initialize logger
logger = logging.getLogger(__name__)

product_fields = {
    "id": fields.Integer, 
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "category_id": fields.Integer,
    "image_url": fields.String
}

class ProductList(Resource):
    @marshal_with(product_fields)
    def get(self):
        products = ProductModel.query.all()
        return products
    

class Product(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, help='This field cannot be blank', required=True)
        self.parser.add_argument('description', type=str, help='This field cannot be blank', required=True)
        self.parser.add_argument('price', type=float, help='This field cannot be blank', required=True)
        self.parser.add_argument('category_id', type=int, help='This field cannot be blank', required=True)
        self.parser.add_argument('image_url', type=str, help='This field cannot be blank', required=True)

    @marshal_with(product_fields)
    def get(self, id=None, user_id=None):
        if user_id:
            products = ProductModel.query.filter_by(user_id=user_id).all()
            return products
        elif id:
            product = ProductModel.query.filter_by(id=id).first()
            if product:
                return product
            else:
                abort(404, message="Product not found")
        else:
            abort(400, message="Please provide either product id or user_id")
    # @jwt_required()
    def post(self):
        # if current_user['role'] != 'admin':
        #     return { "message":"Unauthorized request"}
        args = self.parser.parse_args()
        existing_product = ProductModel.query.filter_by(title=args['title']).first()
        if existing_product:
            abort(404, message="Product already exists")
        else:
            product = ProductModel(**args)
            db.session.add(product)
            db.session.commit()
            return {"message": "Product created successfully"}

    def put(self, id):
        data = request.get_json()
        product = ProductModel.query.get(id)
        if not product:
            abort(404, error="Product not found")

        try:
            for key, value in data.items():  # Update each field individually
                setattr(product, key, value)
            db.session.commit()
            return {"message": f"Product {id} updated successfully"}
        except Exception as e:
            logger.error(f"Error updating product {id}: {str(e)}")
            abort(500, error=f"Update for product {id} unsuccessful")

    def delete(self, id):
        product = ProductModel.query.get(id)
        if not product:
            abort(404, error="Product not found")

        try:
            db.session.delete(product)
            db.session.commit()
            return {"message": f"Product {id} deleted successfully"}
        except Exception as e:
            logger.error(f"Error deleting product {id}: {str(e)}")
            abort(500, error=f"Deletion for product {id} unsuccessful")
