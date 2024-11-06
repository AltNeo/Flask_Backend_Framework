import boto3
from flask import Flask, request, jsonify, session
from flask_mysqldb import MySQL 
import urllib.parse

app = Flask(__name__)

# Initialize Flask-MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'prime')
mysql = MySQL(app)

# Initialize Boto3 S3 client
s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

#Checking admin admin_token
'''
admin_token = session.get('admin_token')
# Check if the admin token exists in the session
if admin_token:
    # Use the admin token for further processing
    print("Admin Token:", admin_token)
else:
    print("Admin Token not found in session")
'''
from flask import session

@app.route('/add_product', methods=['POST'])
def add_product():
    required_fields = ['name', 'price', 'descr', 'stock', 'category_id', 'estimated_price', 'material', 'margin', 'displaystate', 'color']
    missing_fields = [field for field in required_fields if field not in request.form]
    if missing_fields:
        return jsonify({"success": False, "message": f"Missing fields: {', '.join(missing_fields)}"}), 400

    admin_token = session.get('admin_token')
    admin_user_id = session.get('admin_user_id')  # Assuming you store the user's ID in the session

    if admin_token:
        # Admin token exists in the session, proceed with adding the product
        name = request.form['name']
        price = request.form['price']
        descr = request.form['descr']
        stock = request.form['stock']
        category_id = request.form['category_id']
        estimated_price = request.form['estimated_price']
        GSM = request.form.get('GSM')
        material = request.form['material']
        margin = request.form['margin']
        displaystate = request.form['displaystate']
        color = request.form['color']
        tags = request.form.get('tags', '')  # Get tags from form data, default to empty string
        images = request.files.getlist('images')

        cursor = mysql.connection.cursor()
        
        import urllib.parse

        # Handle images
        image_links = []
        for image in images:
            image_key = f"product_images/{name}/{color}/{image.filename}"
            # URL encode the image_key to handle spaces and special characters
            encoded_image_key = urllib.parse.quote(image_key)
            try:
                s3.upload_fileobj(image, 'productimagesprintonia', image_key, ExtraArgs={'ACL': 'public-read'})  # Use the original key for uploading and set it to be publicly readable
                # Construct the URL with the encoded key
                image_url = f"https://productimagesprintonia.s3.ap-southeast-2.amazonaws.com/{encoded_image_key}"
                image_links.append(image_url)
                print(f"Uploaded image to S3 with public access: {image_url}")  # Debugging output
            except Exception as e:
                print(f"Failed to upload image to S3: {e}")  # Error handling

        # Insert product
        if image_links:  # Ensure there are image links before attempting to insert
            query = "INSERT INTO Product (name, price, descr, stock, category_id, estimated_price, GSM, material, margin, displaystate, color, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, price, descr, stock, category_id, estimated_price, GSM, material, margin, displaystate, color, ','.join(image_links)))
            product_id = cursor.lastrowid  # Get the ID of the newly created product
            print(f"Product added with ID: {product_id}")  # Debugging output
        else:
            print("No images were uploaded, product not added.")
            
        # Handle tags
        tag_list = [tag.strip() for tag in tags.split(',')]  # Split tags by comma and strip whitespace
        for tag in tag_list:
            # Check if tag exists
            cursor.execute("SELECT tag_id FROM Tags WHERE tag_name = %s", (tag,))
            tag_record = cursor.fetchone()
            if tag_record:
                tag_id = tag_record[0]
            else:
                # Insert new tag
                cursor.execute("INSERT INTO Tags (tag_name) VALUES (%s)", (tag,))
                tag_id = cursor.lastrowid
            # Link tag to product
            cursor.execute("INSERT INTO Product_Tags (product_id, tag_id) VALUES (%s, %s)", (product_id, tag_id))

        # Log the creation in the audit table
        admin_name = session.get('admin_name')  # Retrieve the admin's name from the session
        audit_query = "INSERT INTO ProductAudit (product_id, action_type, performed_by) VALUES (%s, 'CREATE', %s)"
        cursor.execute(audit_query, (product_id, admin_name))

        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True, "message": "Product added successfully", "image_links": image_links}), 200
    else:
        return jsonify({"success": False, "message": "Unauthorized access"}), 401
    
@app.route('/get_tags', methods=['GET'])
def get_tags():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT tag_name FROM Tags")
    tags = cursor.fetchall()
    cursor.close()
    return jsonify([tag[0] for tag in tags])   

 
    
@app.route('/update_product', methods=['POST'])
def update_product():
    admin_token = session.get('admin_token')
    if admin_token:
        product_id = request.form['product_id']
        data = {key: request.form[key] for key in request.form if key != 'product_id'}
        cursor = mysql.connection.cursor()
        placeholders = ', '.join([f"{key} = %s" for key in data])
        values = tuple(data.values()) + (product_id,)
        query = f"UPDATE Product SET {placeholders} WHERE id = %s"
        cursor.execute(query, values)
        for color, image in zip(request.form.getlist('colors'), request.files.getlist('images')):
            image_key = f"product_images/{product_id}/{color}/{image.filename}"
            s3.upload_fileobj(image, 'productimagesprintonia', image_key)
            query = "INSERT INTO ProductImage (product_id, product_color, image_key) VALUES (%s, %s, %s)"
            cursor.execute(query, (product_id, color, image_key))
        mysql.connection.commit()
        cursor.close()
###TESTING LEFT ABHI
    
@app.route('/get_customers', methods=['GET'])
def customer_list():
    cursor = mysql.connection.cursor()
    query = "SELECT customer_id, name, phone FROM Customer"
    cursor.execute(query)
    customers = cursor.fetchall()
    cursor.close()
    return jsonify(customers)

@app.route('/get_customer_detail', methods=['POST','GET'])
def customer_detail():
    phone = request.form.get('phone')
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Customer WHERE phone = %s"
    cursor.execute(query, (phone,))
    customer = cursor.fetchone()
    cursor.close()
    
    if customer:
        customer_details = {
            "customer_id": customer[0],
            "name": customer[1],
            "email": customer[2],
            "phone": customer[3],
            "main_address": customer[4],
            "Latest Enquiry":customer[6],
            "Order History":customer[7]
        }
        return jsonify(customer_details)
    else:
        return jsonify({"message": "Customer not found"}), 404
    
@app.route('/order_history', methods=['GET'])
def order_history():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM OrderHistory"
    cursor.execute(query)
    orders = cursor.fetchall()
    cursor.close()
    
    order_history_list = []
    for order in orders:
        order_details = {
            "order_id": order[0],
            "customer_id": order[1],
            "shipping_address": order[2],
            "customer_address": order[3],
            "order_date": order[4],
            "contact_number": order[5],
            "payment_id": order[6],
            "enquiry_id": order[7]
        }
        order_history_list.append(order_details)
    
    return jsonify(order_history_list)

@app.route('/display_enquiries', methods=['GET'])
def display_enquiries():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Enquiry"
    cursor.execute(query)
    enquiries = cursor.fetchall()
    
    enquiry_list = []
    for enquiry in enquiries:
        enquiry_details = {
            "enquiry_id": enquiry[0],
            "customer_id": enquiry[1],
            "created_at": enquiry[2],
            "response": enquiry[3],
            "response_date": enquiry[4],
            "design_upload": enquiry[5],
            "enquiry_text": enquiry[6],
            "enquiry_quantity": enquiry[7],
            "enquiry_status": enquiry[8],
            "enquiry_quote": enquiry[9],
            "product_id": enquiry[10]
        }
        
        # Fetch product name based on product_id
        cursor.execute("SELECT name FROM Product WHERE product_id = %s", (enquiry[10],))
        product_name = cursor.fetchone()
        if product_name:
            enquiry_details["product_name"] = product_name[0]
        
        # Fetch customer name based on customer_id
        cursor.execute("SELECT name FROM Customer WHERE customer_id = %s", (enquiry[1],))
        customer_name = cursor.fetchone()
        if customer_name:
            enquiry_details["customer_name"] = customer_name[0]
        
        enquiry_list.append(enquiry_details)
    
    cursor.close()
    
    return jsonify(enquiry_list)


import time

@app.route('/create_enquiry', methods=['POST'])
def create_enquiry():
    product_id = request.form.get('product_id')
    enquiry_text = request.form['enquiry_text']
    enquiry_quantity = request.form['enquiry_quantity']
    
    # Retrieve customer_id from session token
    customer_id = session.get('customer_id')
    
    # Set default enquiry status to "pending"
    enquiry_status = "pending"
    
    # Generate enquiry_id as timestamp + customer_id
    enquiry_id = str(int(time.time())) + str(customer_id)
    
    # Fetch product name based on product_id
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name FROM Product WHERE product_id = %s", (product_id,))
    product_name = cursor.fetchone()
    
    if product_name:
        design_files = request.files.getlist('design_files')
        design_urls = []
        for design_file in design_files:
            design_key = f"design_files/{enquiry_id}/{design_file.filename}"
            encoded_design_key = urllib.parse.quote(design_key)
            try:
                s3.upload_fileobj(design_file, 'printoniaenquiryimages', design_key, ExtraArgs={'ACL': 'public-read'})
                design_url = f"https://printoniaenquiryimages.s3.ap-southeast-2.amazonaws.com/{encoded_design_key}"
                design_urls.append(design_url)
                print(f"Uploaded design file to S3: {design_url}")
            except Exception as e:
                print(f"Failed to upload design file to S3: {e}")
        product_name = product_name[0]
        
        # Insert the enquiry details into the Enquiry table
        # Insert the enquiry details into the Enquiry table
        cursor.execute("INSERT INTO Enquiry (enquiry_id, customer_id, product_id, enquiry_text, enquiry_quantity, enquiry_status, design_upload) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               (enquiry_id, customer_id, product_id, enquiry_text, enquiry_quantity, enquiry_status, ','.join(design_urls)))
        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"success": True, "message": "Enquiry created successfully", "product_name": product_name, "Enquiry_id": enquiry_id})
    else:
        cursor.close()
        return jsonify({"success": False, "message": "Product not found"})


if __name__ == "__main__":
    app.run(debug=True)


