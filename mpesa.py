from requests.auth import HTTPBasicAuth
from datetime import datetime
import requests
import base64
import math
# import time
# import os
# from dotenv import load_dotenv

# load_dotenv()

# consumer_key = os.getenv("consumer_key")
# consumer_secret = os.getenv("consumer_secret")
# api_url = os.getenv("api_url")
# saf_stk_push_url = os.getenv("saf_stk_push_url")
# saf_api_url = os.getenv("saf_api_url")

consumer_key = "kIM7nhs5kDq6YfzbN15kl2LMOX7zlEZ8lZAiA2lM9I0SKcIe"
consumer_secret = "cOByOXYGzn7CAQtjNWTZH71XwKV9c777ssXbaJbrmngzUMAkLY2uNkGvaLW4qU5o"

saf_stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
saf_api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
short_code = "174379"
pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
my_callback_url = "https://nonobligatory-microseismic-bernardo.ngrok-free.dev/stk-call-back"

# time will be sent to stk push
# the request is for  dending http like loads
# math is for converting the interger
# base 64 is for hashing for security
# http basicAuth is used to get token for authentication


def get_mpesa_access_token():
    try:
        res = requests.get(
            saf_api_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
        )
        token = res.json()['access_token']

    except Exception as e:
        print(str(e), "error getting access token")
        raise e

    return token


myToken = get_mpesa_access_token()
print(myToken)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

headers = {
    "Authorization": f"Bearer {myToken}",
    "Content-Type": "application/json"
}


def generate_password():
    password_str = short_code + pass_key + timestamp
    password_bytes = password_str.encode()

    return base64.b64encode(password_bytes).decode("utf-8")


password = generate_password()
print(password)


def make_stk_push(payload):
    amount = payload['amount']
    phone_number = payload['phone_number']
    push_data = {
        "BusinessShortCode": short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": math.ceil(float(amount)),
        "PartyA": phone_number,
        "PartyB": short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": my_callback_url,
        "AccountReference": payload['sale_id'],
        "TransactionDesc": "description of the transaction",
    }
    response = requests.post(
        saf_stk_push_url,
        json=push_data,
        headers=headers)

    response_data = response.json()

    return response_data


c = make_stk_push(
    {"amount": "1", "phone_number": "254714391137", "sale_id": "SALE001"})
print(c)
