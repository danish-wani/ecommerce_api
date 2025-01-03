# E-commerce REST API

A production-grade RESTful API built with Django REST Framework for an e-commerce platform. The API provides endpoints for product management and order processing with JWT authentication.

## Features

- JWT Authentication
- Product Management (CRUD operations)
- Order Processing with Stock Management
- Automated Data Population
- Comprehensive Test Coverage
- Dockerized Development and Deployment
- PostgreSQL Database

## Tech Stack

- Python 3.11
- Django 5.0.1
- Django REST Framework 3.14.0
- PostgreSQL 13
- Docker & Docker Compose
- JWT Authentication (djangorestframework-simplejwt)

## Project Structure

```
ecommerce_api/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── manage.py
├── postgres/
│   └── init.sql
├── ecommerce_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── products/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── management/
    │   └── commands/
    │       ├── wait_for_db.py
    │       └── populate_db.py
    └── tests/
        ├── test_models.py
        ├── test_views.py
        └── test_serializers.py
```

## Prerequisites

- Docker
- Docker Compose
- Git

## Installation & Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce_api
```

2. Create `.env` file in the project root:
```bash
DEBUG=1
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
POSTGRES_DB=ecommerce_db
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=secure_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Apply database migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Populate the database with sample data:
```bash
docker-compose exec web python manage.py populate_db
```

## API Endpoints

### Authentication Endpoints
- POST `/api/token/` - Obtain JWT token pair
- POST `/api/token/refresh/` - Refresh JWT token

### Product Endpoints
- GET `/api/products/` - List all products
- POST `/api/products/` - Create a new product
- GET `/api/products/{id}/` - Retrieve a specific product
- PUT `/api/products/{id}/` - Update a product
- DELETE `/api/products/{id}/` - Delete a product

### Order Endpoints
- GET `/api/orders/` - List all orders
- POST `/api/orders/` - Create a new order
- GET `/api/orders/{id}/` - Retrieve a specific order

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Obtain a token pair:
```bash
curl -X POST http://localhost:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
```

2. Use the access token in subsequent requests:
```bash
curl -H "Authorization: Bearer <your_access_token>" \
     http://localhost:8000/api/products/
```

3. Refresh the token when it expires:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh":"<your_refresh_token>"}'
```

## Testing

### Setting Up Testing Environment

1. Create a `pytest.ini` file in the project root:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = ecommerce_api.settings
python_files = tests.py test_*.py *_tests.py
addopts = -v -s --disable-warnings
```

2. Add pytest dependencies to requirements.txt:
```
pytest==7.4.4
pytest-django==4.7.0
pytest-cov==4.1.0
```

### Running Tests

Using pytest:
```bash

# Run all tests
docker-compose exec web pytest

# Run tests with verbose output
docker-compose exec web pytest -v

# Run specific test file
docker-compose exec web pytest products/tests/test_models.py

# Run specific test class
docker-compose exec web pytest products/tests/test_models.py::ProductModelTest

# Run specific test method
docker-compose exec web pytest products/tests/test_models.py::ProductModelTest::test_product_creation

# Run tests with coverage report
docker-compose exec web pytest --cov=products

# Generate HTML coverage report
docker-compose exec web pytest --cov=products --cov-report=html
```

### Test Categories

Our test suite includes:

1. Model Tests (`test_models.py`)
   - Product model validation
   - Order model validation
   - OrderItem relationships
   - Price and stock constraints

2. View Tests (`test_views.py`)
   - API endpoint functionality
   - Authentication
   - Permission checks
   - Response formats

## Data Models

### Product
- id (integer, unique)
- name (string)
- description (string)
- price (decimal)
- stock (integer)

### Order
- id (integer, unique)
- total_price (decimal)
- status (string: 'pending' or 'completed')
- created_at (datetime)
- updated_at (datetime)

### OrderItem
- order (foreign key to Order)
- product (foreign key to Product)
- quantity (integer)
- price (decimal)

## Development

### Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and update tests as needed

3. Run tests to ensure everything works:
```bash
docker-compose exec web python manage.py test
```

4. Apply any new migrations:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Database Management

Reset the database:
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d   # Restart containers
docker-compose exec web python manage.py migrate  # Apply migrations
docker-compose exec web python manage.py populate_db  # Repopulate data
```

### Accessing PostgreSQL

Connect to the database:
```bash
docker-compose exec db psql -U ecommerce_user -d ecommerce_db
```

Common PostgreSQL commands:
```sql
\l           -- List databases
\dt          -- List tables
\d tablename -- Describe table
\q           -- Quit
```

## Production Deployment

For production deployment:

1. Update `.env` file with production values:
```bash
DEBUG=0
SECRET_KEY=your-secure-secret-key
DJANGO_ALLOWED_HOSTS=your-domain.com
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_secure_password
```

2. Build the production image:
```bash
docker-compose -f docker-compose.prod.yml build
```

3. Deploy using your preferred hosting service

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Debug mode | 1 |
| SECRET_KEY | Django secret key | None |
| DJANGO_ALLOWED_HOSTS | Allowed hosts | localhost 127.0.0.1 |
| POSTGRES_DB | Database name | ecommerce_db |
| POSTGRES_USER | Database user | ecommerce_user |
| POSTGRES_PASSWORD | Database password | secure_password |
| POSTGRES_HOST | Database host | db |
| POSTGRES_PORT | Database port | 5432 |

## Troubleshooting

### Common Issues

1. Database connection errors:
   - Check if PostgreSQL container is running
   - Verify database credentials in .env file
   - Ensure the database host is correctly set

2. Migration issues:
   - Remove all migrations and start fresh
   - Reset the database using the commands in Database Management section

3. Permission issues:
   - Check if you're authenticated
   - Verify your token hasn't expired
   - Ensure you're using the correct authorization header

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

The project license is to be added.