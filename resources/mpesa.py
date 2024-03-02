from flask import request, jsonify
from flask_restful import Resource, Api
import requests
import base64
import datetime


CONSUMER_KEY = 'wBnjllVp4EAyDPlai2AkrsmRI562l4TY3qn895iKajs2odSI'
CONSUMER_SECRET = 'WZgAqaxQi7fpzipvCCUTXGELg6W3dtxiAGFZGZ3vfXkOnRjGiQuCkKxaIeII66O4'
LIPA_NA_MPESA_ONLINE_PASSKEY = 'your_passkey'
LIPA_NA_MPESA_ONLINE_SHORTCODE = '600978'
CALLBACK_URL = 'your_ngrok_url/mpesa/callback'  # Ngrok URL or your deployed URL

class STKPushResource(Resource):
    def post(self):
        try:
            phone_number = request.json.get('phoneNumber')
            amount = request.json.get('amount')

            access_token = generate_access_token()
            response = initiate_stk_push(phone_number, amount, access_token)

            return {'status': 'success', 'response': response}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

class CallbackResource(Resource):
    def post(self):
        # Handle M-Pesa callback logic here
        print(request.json)
        return '', 200



def generate_access_token():
    url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    credentials = f'{CONSUMER_KEY}:{CONSUMER_SECRET}'
    credentials_base64 = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': 'Basic ' + credentials_base64
    }

    response = requests.get(url, headers=headers)
    access_token = response.json().get('access_token')
    return access_token

def initiate_stk_push(phone_number, amount, access_token):
    url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
    }

    payload = {
        'BusinessShortCode': LIPA_NA_MPESA_ONLINE_SHORTCODE,
        'Password': generate_password(LIPA_NA_MPESA_ONLINE_SHORTCODE, LIPA_NA_MPESA_ONLINE_PASSKEY),
        'Timestamp': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': 1,
        'PartyA': 254708374149,
        'PartyB': 174379,
        'PhoneNumber': 254708374149,
        'CallBackURL': 'https://mydomain.com/path',
        'AccountReference': 'CompanyXLTD',
        'TransactionDesc': 'Payment for services',
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def generate_password(shortcode, passkey):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password_string = f'{shortcode}{passkey}{timestamp}'
    encoded_password = base64.b64encode(password_string.encode()).decode()
    return encoded_password

