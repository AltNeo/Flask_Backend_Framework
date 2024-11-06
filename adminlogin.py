import os  # Add this import
from flask import Flask, request, session, jsonify
from flask_session import Session
import random
import json
import string
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp'
Session(app)

# Initialize Flask-MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'prime')
mysql = MySQL(app)

# API fetch commands go here 

from itsdangerous import URLSafeTimedSerializer

@app.route('/admin_login', methods=['POST'])

def login():
    # Get the form data
    email = request.form.get('email')
    provided_password = request.form.get('password')
    
    if not email or not provided_password:
        return jsonify({"success": False, "message": "Email or password field is missing"}), 400
    
    cursor = mysql.connection.cursor()
    query = "SELECT admin_pass, name FROM adminlogin WHERE admin_mail = %s;"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    stored_password, admin_username = user
    if provided_password == stored_password:
        # Generate a session token
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = s.dumps({'admin_email': email})
        
        # Store the token and the admin's name in the session
        session['admin_token'] = token
        session['admin_name'] = admin_username  # Storing the name in the session
        
        # Return the token and the admin's username in the JSON response
        return jsonify({"success": True, "message": "Login successful", "token": token, "admin_username": admin_username}), 200
    else:
        return jsonify({"success": False, "message": "Invalid password"}), 401


@app.route('/admin_logout', methods=['POST'])
def logout():
    # Remove the token from the session
    session.pop('admin_token', None)
    
    # Return a success message
    return jsonify({"success": True, "message": "Logout successful"}), 200

@app.route('/adminhw' )
def helloworld():
    admin_token = session.get('admin_token')
    if admin_token:
        return jsonify({"success": True, "message": "Session exists", "token": admin_token}), 200
    else:
        return jsonify({"success": False, "message": "Session does not exist"}), 401


    
if __name__ == "__main__":
    app.run(debug=True)
