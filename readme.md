# Flask Backend Framework

A robust Flask-based backend framework providing essential features for web applications.

## Features

- **Authentication System**
  - OTP-based user authentication
  - Session management
  - Admin authentication

- **Product Management**
  - CRUD operations for products
  - Category management
  - Image upload to AWS S3
  - Product search and filtering

- **Admin Panel**
  - User management
  - Order tracking
  - Enquiry system
  - Analytics dashboard

- **Security Features**
  - Session-based authentication
  - Environment variable configuration
  - Secure password handling

## Tech Stack

- Python 3.x
- Flask
- MySQL
- AWS S3 for storage
- Flask-Session for session management

## Setup

1. Clone the repository
```bash
git clone https://github.com/AltNeo/Flask_Backend_Framework.git
cd Flask_Backend_Framework
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Environment Setup
- Copy `.env.example` to `.env`
- Update the variables in `.env` with your configuration:
  - Database credentials
  - AWS credentials
  - Secret keys
  - API configurations

5. Database Setup
- Run the SQL scripts in order:
  1. `Database Creation.sql`
  2. Required dummy data scripts from DatabaseStructure/

## API Documentation

### Authentication Endpoints
- `POST /generate_otp` - Generate OTP for login
- `POST /user_login` - User login with OTP
- `POST /user_logout` - User logout
- `POST /admin_login` - Admin login

### Product Endpoints
- `GET /get_products` - List products
- `GET /get_individual_product` - Get product details
- `GET /get_categories` - List categories
- `GET /get_categorywise_products` - Get products by category
- `POST /add_product` - Add new product (Admin)
- `POST /update_product` - Update product (Admin)

### Admin Endpoints
- `GET /order_history` - View order history
- `GET /display_enquiries` - View customer enquiries
- `POST /create_enquiry` - Create new enquiry

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.






1. Error Handling & Logging
- Add comprehensive error handling
- Implement proper logging system
- Add request validation



3. Code Structure
- Organize code into blueprints
- Create proper config management
- Add unit tests
- Implement dependency injection

4. Documentation
- Add docstrings to functions
- Create API documentation using Swagger/OpenAPI
- Add code comments

5. Performance
- Add caching layer
- Implement database connection pooling
- Add database migrations support