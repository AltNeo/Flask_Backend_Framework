from urllib import response
from flask import Flask, request, session, jsonify
from flask_session import Session
import admin_api, adminlogin
import random
import json
import string
from flask import Flask
import urllib.parse
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kg9b6irasp'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp'
Session(app)

# Initialize Flask-MySQL

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'prime')

'''
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12918555'
app.config['MYSQL_DB'] = 'dummy'
'''
mysql = MySQL(app)

# API fetch commands go here

from flask import jsonify
## No Login APIs

@app.route('/get_products', methods=['GET'])
def get_products():
    try:
        print("Fetching top 10 products...")
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT p.product_id, p.name, p.images AS imagelink, p.price, c.category_name 
            FROM Product p 
            LEFT JOIN ProductImage pi ON p.product_id = pi.product_id
            JOIN Category c ON p.category_id = c.category_id
            WHERE p.displaystate = 1
            ORDER BY p.product_id ASC
            LIMIT 10
        """)
        products = cursor.fetchall()
        
        # Get column names and convert them to strings
        columns = [column[0] for column in cursor.description]

        # Create a list of dictionaries with column names as keys
        result = []
        for product in products:
            product_info = dict(zip(map(str, columns), product))
            result.append(product_info)
        
        cursor.close()
        print("Top 10 products fetched.")
        print(result)
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#New Change
@app.route('/get_individual_product', methods=['POST'])
def get_individual_product():
    try:
        product_id = request.form['product_id']
        print(f"Fetching product with ID: {product_id}...")
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT p.*, pi.product_color, pi.image_key 
            FROM Product p 
            LEFT JOIN ProductImage pi ON p.product_id = pi.product_id
            WHERE p.product_id = %s AND p.displaystate = 1
        """, (product_id,))
        product = cursor.fetchone()

        if product:
            # Get column names and convert them to strings
            columns = [column[0] for column in cursor.description]

            # Create a dictionary with column names as keys
            product_info = dict(zip(map(str, columns), product))
            # Check if product has images
            if product_info.get('product_color') and product_info.get('image_key'):
                color = product_info.pop('product_color')  # Remove color from product_info
                image_key = product_info.pop('image_key')  # Remove image_key from product_info
                # Add color and image_key to product_info under 'images' dictionary
                product_info.setdefault('images', {}).setdefault(color, []).append(image_key)

            cursor.close()
            print("Product fetched.")
            print(product_info)
            return jsonify({"success": True, "data": product_info}), 200
        else:
            cursor.close()
            return jsonify({"success": False, "message": "Product not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    



@app.route('/get_categories', methods=['GET'])
def get_categories():
    try:
        print("Fetching categories...")
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM Category")
        categories = cursor.fetchall()
        
        # Get column names and convert them to strings
        columns = [column[0] for column in cursor.description]
        
        # Create a list of dictionaries with column names as keys
        result = []
        for category in categories:
            result.append(dict(zip(map(str, columns), category)))
        cursor.close()
        print("Categories fetched.")
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
    
@app.route('/get_categorywise_products', methods=['GET'])
def categorywise_products():
    print("Fetching categorywise products...")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT p.*, c.category_name FROM Product p JOIN Category c ON p.category_id = c.category_id ORDER BY p.category_id;")
    categorywise_products = cursor.fetchall()
    
    # Get column names and convert them to strings
    columns = [column[0] for column in cursor.description]

    # Create a list of dictionaries with column names as keys
    result = []
    for product in categorywise_products:
        result.append(dict(zip(map(str, columns), product)))
    cursor.close()
    print("Categorywise products fetched.")
    return jsonify(result)



def top_products():
    print("Fetching top products...")
    conn = mysql.connect()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Category")
    top_prods = cur.fetchall()
    cur.close()
    conn.close()
    print("Top products fetched.")
    return jsonify(top_prods)


@app.route('/search')
def search_product():
    print("Searching for products...")
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    limit = per_page
    conn = mysql.connect()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Product WHERE name LIKE %s LIMIT %s OFFSET %s", ('%' + query + '%', limit, offset))
    products = cur.fetchall()
    cur.close()
    conn.close()
    print("Products searched.")
    return jsonify(products)
## User APIs
import otp
@app.route('/generate_otp', methods=['POST'])
def trigger_generate_otp():
    response=otp.generate_otp()
    return response


@app.route('/user_login', methods=['POST'])
def user_login():
    response=otp.user_login()
    return response

@app.route('/user_logout', methods=['POST'])
def user_logout():
    response=otp.logout()
    return response

@app.route('/checksessiontoken', methods=['GET'])
def gettoken():
    token=otp.gettoken()
    return token

@app.route('/show_session', methods=['GET'])
def get_session_details():
    response=otp.get_session_details()
    return response

## Admin APIs
from itsdangerous import URLSafeTimedSerializer

@app.route('/admin_login', methods=['POST'])
def login():
    response=adminlogin.login()
    return response

@app.route('/admin_logout', methods=['POST'])
def logout():
    response=adminlogin.logout()
    return response

@app.route('/adminhw', methods=['GET'])
def hellow():
    admin_token = session.get('admin_token')
    if admin_token:
        return jsonify({"success": True, "message": "Session exists", "token": admin_token}), 200
    else:
        return jsonify({"success": False, "message": "Session does not exist"}), 401


@app.route('/add_product', methods=['POST'])
def add_prod():
    response = admin_api.add_product()
    return response

@app.route('/update_product', methods=['POST'])
def update_product():
    response=admin_api.update_product()
    return response

@app.route('/order_history', methods=['GET'])
def order_his():
    response=admin_api.order_history()
    return response

@app.route('/display_enquiries', methods=['GET'])
def display_enquiries():
    response=admin_api.display_enquiries()
    return response

@app.route('/create_enquiry', methods=['POST'])
def create_enquiry():
    response=admin_api.create_enquiry()
    return response
'''

@app.route('/get_customers', methods=['GET'])
def customer_list():
    response=admin_api.customer_list()
    return response

@app.route('/get_customer_detail', methods=['POST','GET'])
def customer_detail():
    response=admin_api.customer_detail()
    return response
'''

##TESTING
@app.route('/')
def helloworld():
    return "Hello, World!"



if __name__ == "__main__":
    app.run(debug=True)