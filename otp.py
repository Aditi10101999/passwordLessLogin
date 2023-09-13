from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
from twilio.rest import Client
import random

from db_connect import connect_to_db, insert_data, select_data, select_otp_data, update_otp_data

app = Flask(__name__)

# Replace these values with your Twilio credentials
TWILIO_ACCOUNT_SID = 'ACc2b07aaaae38687535e47a8ecac506b4'
TWILIO_AUTH_TOKEN = '006c6be328da973875a7ea94643a040d'
TWILIO_PHONE_NUMBER = '+12568576480'

# In-memory storage for OTPs (in production, use a database)
otp_storage = {}

@app.route('/send_otp', methods=['POST'])
def send_otp():
    try:
        mobile_number = "+91"+request.json['mobile_number']
    except KeyError:
        return jsonify({'error': 'Mobile number is required'}), 400

    

    db_var=connect_to_db('localhost', 'postgres','postgres', 'Neebal#98760', 5432)
    number_check=select_data(db_var[0],mobile_number)
    num_check=len(number_check)

    if num_check>0:

        # Generate a random 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Store the OTP in memory
        otp_storage[mobile_number] = otp
        print(otp)
        # Send OTP via Twilio SMS
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f'Your OTP is: {otp}',
            from_=TWILIO_PHONE_NUMBER,
            to=mobile_number
        )
        response_statement={'message': 'OTP sent successfully'}
        status=200


        user_data=[number_check[0][0],str(mobile_number).replace('+',''),otp]
        select_otp=select_otp_data(db_var[0],mobile_number)
        print(select_otp)
        insert_data(db_var[0],db_var[1],user_data)
        # if len(select_otp)>0:
        #     update_otp_data(db_var[0],db_var[1],str(mobile_number).replace('+',''),str(otp))
        # elif len(select_otp)==0:
        #     insert_data(db_var[0],db_var[1],user_data)
    elif num_check==0:
        response_statement={'message': 'Enter Valid Mobile Number'}
        status=400




    return jsonify(response_statement), status

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    try:
        mobile_number = "+91"+request.json['mobile_number']
        entered_otp = request.json['otp']
    except KeyError:
        return jsonify({'error': 'Mobile number and OTP are required'}), 400

    stored_otp = otp_storage.get(mobile_number)

    if not stored_otp:
        return jsonify({'error': 'OTP not found. Please request a new OTP'}), 401

    if entered_otp == stored_otp:
        # Successful login
        del otp_storage[mobile_number]
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid OTP'}), 401


# Allow requests only from "http://example.com"
CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})


if __name__ == '__main__':
    app.run(debug=True)


