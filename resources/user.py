from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required,  current_user, create_access_token, create_refresh_token, get_jwt_identity

from functools import wraps
from models import db, UserModel

bcrypt=Bcrypt()

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'address': fields.String,
    'phone_number': fields.String,
    'role': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime	
}

response_field={
    "message":fields.String,
    "status":fields.String,
    "user":fields.Nested(user_fields)
}

class SignUpResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="Username is required")
    parser.add_argument('email',  required=True, help="Email is required")
    parser.add_argument('phone_number', required=True, help="Phone number is required")
    parser.add_argument('address', required=True, help="Address is required")
    parser.add_argument('role', required=False, help="Role is required")
    parser.add_argument('password', required=True, help="Password is required")

    @marshal_with(user_fields)
    #@jwt_required()     
    def get(self, id=None):
        # current_user = get_jwt_identity()
        if id:
            user=UserModel.query.filter_by(id=id).first()
            if user is not None:
                return user, 200 
            else:
                abort(404, error="User does not exist")
    
        else:
            users= UserModel.query.all()
            return users
    
    @marshal_with(response_field)
    def post(self):
        data = SignUpResource.parser.parse_args()
        print(f"Received data: {data}")
        print(bcrypt.generate_password_hash(data['password'], 10))
        print(bcrypt.generate_password_hash(data['password'], 10))
        data['password'] = bcrypt.generate_password_hash(data['password'], 10)
        # data['role']= 'member'
        valid_roles = ['member', 'admin']
        if data['role'] not in valid_roles:
            abort(400, error="Invalid role. Allowed roles are 'member' or 'admin'.")

        user = UserModel(**data)
        email = UserModel.query.filter_by(email=data['email']).first()

        if email:
            abort(403, error="Email address already exists")
        phone = UserModel.query.filter_by(phone_number=data['phone_number']).first()
        if phone:
            abort(403, error="Phone number already exists")

        try:
            db.session.add(user)
            db.session.commit()
            return {"message": "User created successfully"}, 201
        except Exception as e:
            print(f"Error during user creation: {str(e)}")
            db.session.rollback()  # Rollback changes in case of an error
            abort(500, error="Unsuccessful creation")




    #@jwt_required()

    def delete(self, id):
        # if current_user['role'] != 'member':
        #     return { "message":"Unauthorized request"}
        user = UserModel.query.get(id)
        if user is None:
            abort(404, error="User not found")            
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User {id} deleted successfully"}
        except Exception as e:
                print(f"Error: {str(e)}")
                abort(500, error=f"Deletion for user {id} unsuccessful")

    def patch(self, id=None):
        if current_user['role'] != 'member':
            return { "message":"Unauthorized request"}
        data = SignUpResource.parser.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if user is None:
            abort(404, error="User not found")
        user.username = data['username']
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.address = data['address']
        user.password = data['password']
        try:
            db.session.commit()
            return {"message": f"User {id} updated successfully"}
        except Exception as e:
            print(f"Error: {str(e)}")
            abort(500, error=f"Update for user {id} unsuccessful")
    

class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help="Email is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data=LoginResource.parser.parse_args()

        user =UserModel.query.filter_by(email= data['email']).first()

        if user:
            is_password_correct = user.check_password(bcrypt, data['password'])

            if is_password_correct:
                user_json=user.to_json()
                access_token=create_access_token(identity=user_json["id"])
                refresh_token=create_refresh_token(identity=user_json["id"])
                return {"message": "login successful", "status":"success", "access_token": access_token, "refresh_token": refresh_token, "user":user_json}, 200
            
            else:
               return {"message": "invalid email/password", "status":"fail"}, 403
        else:
            return {"message": "invalid email/password", "status":"fail"}, 403

        

    # def admin_required(self):
    #     def wrapper(fn):
    #         @wraps(fn)
    #         def decorator(*args, **kwargs):
    #             current_user = get_jwt_identity()
    #             if current_user.get('role') == 'admin':
    #                 return fn(*args, **kwargs)
    #             else:
    #                 return jsonify(msg="Admins only!"), 403

    #         return decorator
        



        

