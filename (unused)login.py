from flask import Flask, request, session, redirect, url_for, jsonify
from flask_session import Session
import random
import string
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp'
Session(app)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = 'dummy'

# Initialize MySQL
mysql = MySQL(app)



users = {}


@app.route('/login', methods=['POST'])
def login():
    phone_number = request.form.get('phone_number')
    pin = request.form.get('OTP')

    if not phone_number or not pin:
        return 'Phone number and PIN are required', 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE phone_number = %s", (phone_number,))
    user = cursor.fetchone()

    if user and pin == user['pin']:
        session['phone_number'] = phone_number
        session['login_mode'] = user['login_mode']
        session['session_key'] = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
        cursor.execute("UPDATE users SET session_key = %s WHERE phone_number = %s", (session['session_key'], phone_number))
        mysql.connection.commit()
        return 'Logged in successfully'
    else:
        return 'Invalid phone number or PIN', 401

@app.route('/logout')
def logout():
    session.pop('phone_number', None)
    session.pop('login_mode', None)
    session.pop('session_key', None)

    phone_number = session.get('phone_number')
    if phone_number:
        with mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE users SET session_key = NULL WHERE phone_number = %s", (phone_number,))
        mysql.connection.commit()

    return 'Logged out successfully'


if __name__ == '__main__':
    app.run()