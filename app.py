from flask import Flask# , jsonify, request
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
import os
from models import db,UserModel# ,PaymentModel
from resources.category import Category,CategoryList
from resources.user import SignUpResource,LoginResource
from resources.order import Order
from resources.product import Product,ProductList
from flask_jwt_extended import JWTManager
# import requests
from flask_cors import CORS
# from requests.auth import HTTPBasicAuth
# from datetime import datetime
from flask_mail import Mail
from resources.review import ReviewList,Review_id



app = Flask(__name__)


# Configure database URI and disable track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
# postgresql://furniture_gardens_user:UA8fv03mbi0bpQdkw9aVVloP29DDzPZq@dpg-cngh0i7109ks73ftn8v0-a.frankfurt-postgres.render.com/furniture_gardens
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "jwt-secret"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'furnituregareden32@gmail.com'  
app.config['MAIL_PASSWORD'] = 'hasoxasnnvhjupec'   

mail = Mail(app)

migrations=Migrate(app,db)


db.init_app(app)
api=Api(app)
bcrypt=Bcrypt(app)
jwt=JWTManager(app)

CORS(app)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none().to_json()

api.add_resource(SignUpResource, '/users', '/users/<int:id>')
api.add_resource(LoginResource, '/login')

api.add_resource(CategoryList, '/categorylist')
api.add_resource(Category, '/category', '/category/<int:category_id>')
api.add_resource(Product, '/product','/product/<int:id>') 
api.add_resource(ProductList, '/products') 
api.add_resource(ReviewList, '/reviews')
api.add_resource(Review_id, '/reviews/<int:review_id>')
api.add_resource(Order,'/orders','/orders/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# consumer_key = 'FhrGbobA03pQ7Ge6OSXCH8V4SJtmU9zeVqohmHdQBzNhpeyE'
# consumer_secret = 'oysGKHLV5qsTzdblj7BAiYJMXFr5ooJT6kBZun9y18f1Bw6jt1KGyd541VmGGun2'
# base_url = 'http://127.0.0.1:5000'


# def get_mpesa_access_token():
#     mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#     response = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     if response.status_code == 200:
#         return response.json()['access_token']
#     else:
#         return None


# @app.route('/access_token') 
# def access_token():
#     mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#     response = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     return response.json()

# # Route for creating payments
# @app.route('/payments', methods=['POST'])
# def create_payment():
#     data = request.get_json()
#     amount = data.get('amount')
#     payment_type = data.get('payment_type')
#     status = 'Pending' 
#     payment_date = datetime.utcnow()  
#     user_id = data.get('user_id')
#     order_id = data.get('order_id')

 
#     new_payment = PaymentModel(
#         amount=amount,
#         payment_type=payment_type,
#         status=status,
#         payment_date=payment_date,
#         user_id=user_id,
#         order_id=order_id
#     )

#     db.session.add(new_payment)
#     db.session.commit()

   
#     mpesa_access_token = get_mpesa_access_token() 
#     if mpesa_access_token:
        
#         payload = {
#             "shortcode": "600990",
#             'CommandID': 'CustomerPayBillOnline',
#             'Amount': amount,
#             'Msisdn': '254790130352', 
#             "BillRefNumber": "TestPay1",  
#         }

       
#         mpesa_response = requests.post('https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate',
#                                        json=payload,
#                                        headers={'Authorization': 'Bearer ' + mpesa_access_token})

#         if mpesa_response.status_code == 200:
            
#             return jsonify({'message': 'Payment initiated successfully!'}), 201
#         else:
            
#             return jsonify({'message': 'Failed to initiate payment with M-Pesa!'}), 500
#     else:
#         return jsonify({'message': 'Failed to get M-Pesa access token!'}), 500


# @app.route('/payments', methods=['GET'])
# def get_payments():
#     payments = PaymentModel.query.all()
#     return jsonify({'payments': [{'id': payment.id, 'amount': payment.amount} for payment in payments]})

# @app.route('/payments/<int:id>', methods=['GET'])
# def get_payment(id):
#     payment = PaymentModel.query.get_or_404(id)
#     return jsonify({'id': payment.id, 'amount': payment.amount})


# @app.route('/payments/<int:id>', methods=['PATCH'])
# def update_payment(id):
#     payment = PaymentModel.query.get_or_404(id)
#     data = request.get_json()

#     if 'amount' in data:
#         payment.amount = data['amount']
#     if 'payment_type' in data:
#         payment.payment_type = data['payment_type']
#     if 'status' in data:
#         payment.status = data['status']
#     if 'payment_date' in data:
#         payment.payment_date = data['payment_date']
#     if 'user_id' in data:
#         payment.user_id = data['user_id']
#     if 'order_id' in data:
#         payment.order_id = data['order_id']

#     db.session.commit()
#     return jsonify({'message': 'Payment updated successfully!'})


# @app.route('/payments/<int:id>', methods=['DELETE'])
# def delete_payment(id):
#     payment = PaymentModel.query.get_or_404(id)
#     db.session.delete(payment)
#     db.session.commit()
#     return jsonify({'message': 'Payment deleted successfully!'})


# @app.route('/register')
# def register():
#     mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#     headers = {"Authorization": "Bearer %s" % access_token()}

#     response = requests.post(
#         mpesa_endpoint,
#         json={
#             "shortcode": "600990",
#             "ResponseType": "Completed",
#             "ConfirmationUrl": base_url + "/c2b/confirm",
#             "ValidationURL": base_url + "/c2b/validation",
#         },
#         headers=headers
#     )
#     return response.json()

# @app.route("/c2b/confirm")
# def confirm():
#     # get data
#     data = request.get_json()

#     file = open('confirm.json', 'a')
#     file.write(data)
#     file.close()
#     return {
#         "ResultCode": "0",
#         "ResultDesc": "Accepted",
#     }


# @app.route("/c2b/validation")
# def validate():
#     # get data
#     data = request.get_json()

#     file = open('validation.json', 'a')
#     file.write(data)
#     file.close()

#     return {
#         "ResultCode": "0",
#         "ResultDesc": "Accepted",
#     }

# @app.route('/simulate')
# def simulate():
#     mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#     acc_token = access_token()
#     headers = {"Authorization": "Bearer %s" % acc_token}
#     request_body = {
#         "ShortCode": "600988",
#         "CommandID": "CustomerPayBillOnline",
#         "BillRefNumber": "TestPay1",
#         "Msisdn": "254790130352",
#         "Amount": 100
#     }
#     simulate_response = requests.post(mpesa_endpoint, json=request_body, headers=headers)
#     return simulate_response.json()


