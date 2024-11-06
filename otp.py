from flask import Flask, request, session, redirect, url_for, jsonify
from flask_session import Session
import random
import string
from flask_mysqldb import MySQL
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kg9b6irasp'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp'
Session(app)

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'prime')
mysql = MySQL(app)


# Initialize MySQL
mysql = MySQL(app)


@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    phone = request.form.get('phone')

    if not phone:
        return jsonify({"success": False, "message": "Phone number is required", "code": 400}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Customer WHERE phone = %s", (phone,))
    user = cursor.fetchone()

    if not user:
        # Create a new user with phone number and OTP
        cursor.execute("INSERT INTO Customer (phone, pin) VALUES (%s, %s)", (phone, None))
        mysql.connection.commit()

        # Generate a 4-digit random PIN
        pin = '6969'  # For testing purposes, replace with the commented line above in production

        # Update the PIN field in the database
        cursor.execute("UPDATE Customer SET pin = %s WHERE phone = %s", (pin, phone))
        mysql.connection.commit()

        # Send the OTP to the user (you can use an SMS gateway or any other method)
        send_otp_to_user(phone, pin)
        # Add a timestamp for OTP generation
        cursor.execute("UPDATE Customer SET pin = %s, otp_timestamp = %s WHERE phone = %s", (pin, datetime.now(), phone))
        mysql.connection.commit()

        return jsonify({"success": True, "message": "New user created and OTP sent successfully", "code": 200})
        
    if user:
        # Clear the PIN field in the database
        cursor.execute("UPDATE Customer SET pin = NULL WHERE phone = %s", (phone,))
        mysql.connection.commit()

        # Generate a 4-digit random PIN
        #pin = ''.join(random.choices(string.digits, k=4))
        pin = '6969'  # For testing purposes, replace with the commented line above in production

        # Update the PIN field in the database
        cursor.execute("UPDATE Customer SET pin = %s WHERE phone = %s", (pin, phone))
        mysql.connection.commit()

        # Send the OTP to the user (you can use an SMS gateway or any other method)
        send_otp_to_user(phone, pin)
        # Add a timestamp for OTP generation
        cursor.execute("UPDATE Customer SET pin = %s, otp_timestamp = %s WHERE phone = %s", (pin, datetime.now(), phone))
        mysql.connection.commit()
        
        return jsonify({"success": True, "message": "OTP sent successfully", "code": 200})
    else:
        return jsonify({"success": False, "message": "User not found", "code": 404}), 404


@app.route('/user_login', methods=['POST'])
def user_login():
    phone = request.form.get('phone')
    provided_pin = int(request.form.get('pin'))

    if not phone or not provided_pin:
        return jsonify({"success": False, "message": "Phone number and PIN are required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, customer_id, pin, otp_timestamp FROM Customer WHERE phone = %s", (phone,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    stored_username, customer_id, stored_pin, otp_timestamp = user
    
    if stored_pin is None or (datetime.now() - otp_timestamp) > timedelta(minutes=15):
        return jsonify({"success": False, "message": "OTP expired or not generated"}), 401

    if provided_pin == stored_pin:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps({'phone': phone, 'username': stored_username})

        session['user_token'] = token
        session['phone'] = phone
        session['username'] = stored_username
        session['customer_id'] = customer_id

        cursor.execute("UPDATE Customer SET pin = NULL WHERE phone = %s", (phone,))
        mysql.connection.commit()

        return jsonify({"success": True, "message": "Login successful", "token": token}), 200
    else:
        return jsonify({"success": False, "message": "Invalid PIN"}), 401

'''
#DEBUGGING
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/user_login', methods=['POST'])
def user_login():
    phone = request.form.get('phone')
    provided_pin = int(request.form.get('pin'))

    if not phone or not provided_pin:
        logging.debug("Missing phone number or PIN")
        return jsonify({"success": False, "message": "Phone number and PIN are required"}), 400

    cursor = mysql.connection.cursor()
    logging.debug(f"Looking up user with phone number: {phone}")
    cursor.execute("SELECT pin FROM Customer WHERE phone = %s", (phone,))
    user = cursor.fetchone()

    if not user:
        logging.debug("User not found in database")
        return jsonify({"success": False, "message": "User not found"}), 404

    stored_pin = user[0]
    logging.debug(f"Stored PIN: {stored_pin}, Provided PIN: {provided_pin}")
    if provided_pin == stored_pin:
        logging.debug("PIN match found, generating session token")
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps({'phone': phone})

        session['user_token'] = token
        logging.debug(f"Session token generated and stored: {token}")

        return jsonify({"success": True, "message": "Login successful", "token": token}), 200
    else:
        logging.debug("Invalid PIN provided")
        return jsonify({"success": False, "message": "Invalid PIN"}), 401
'''




    
@app.route('/logout', methods=['POST'])
def logout():

    phone = session.get('phone')
    session.clear()
    if phone:
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE Customer SET session_key = NULL WHERE phone = %s", (phone,))
        mysql.connection.commit()

    return 'Logged out successfully'

@app.route('/checksessiontoken', methods=['GET'])
def gettoken():
    token=session.get('user_token')
    if not token:
        return jsonify({"success": False, "message": "Logged out"}), 401
    else:
        return token

def send_otp_to_user(phone, pin):

    print(f"Sending OTP {pin} to {phone}")

def show_session_details():
    session_details = {}
    for key, value in session.items():
        session_details[key] = value
    return jsonify({"success": True, "message": "Session details", "data": session_details}), 200

@app.route('/show_session', methods=['GET'])
def get_session_details():
    return show_session_details()

if __name__ == '__main__':
    app.run(debug=True)