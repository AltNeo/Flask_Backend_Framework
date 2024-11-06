# Printonia Backend

Backend service for Printonia, an e-commerce platform specializing in custom printing and merchandise.

## Features

- Product management (CRUD operations)
- Category management
- User authentication with OTP
- Admin dashboard
- Order tracking
- Enquiry system
- Image upload to AWS S3

## Setup

1. Clone the repository
```bash
git clone [repository-url]
cd BackendDB
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
- Update the variables in `.env` with your configuration

5. Database Setup
- Run the SQL scripts in the following order:
  1. `Database Creation.sql`
  2. Required dummy data scripts from DatabaseStructure/

## Running the Application

```bash
python API.py
```

The server will start on `http://localhost:5000`

## API Documentation

### Public Endpoints
- `GET /get_products` - Fetch top 10 products
- `POST /get_individual_product` - Get product details
- `GET /get_categories` - List all categories
- `GET /get_categorywise_products` - Get products by category

### User Endpoints
- `POST /generate_otp` - Generate OTP for login
- `POST /user_login` - User login with OTP
- `POST /user_logout` - User logout

### Admin Endpoints
- `POST /admin_login` - Admin login
- `POST /add_product` - Add new product
- `POST /update_product` - Update product details
- `GET /order_history` - View order history
- `GET /display_enquiries` - View customer enquiries

## Contributing

1. Create a new branch
2. Make your changes
3. Submit a pull request

## License

[Your License Here]
