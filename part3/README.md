# HBnB Project - Part 2

## Overview
HBnB (Holberton B&B) is a web application that implements core functionalities similar to Airbnb. This project focuses on building the Business Logic and API layers using Python, Flask, and Flask-RESTX.

## Features
- User management (Create, Read, Update)
- Place management (Create, Read, Update)
- Review management (Create, Read, Update, Delete)
- Amenity management (Create, Read, Update)

## Project Structure
```
hbnb/
├── app/                      # Core application code
│   ├── api/                  # API endpoints
│   │   └── v1/              # Version 1 of the API
│   ├── models/              # Business logic classes
│   ├── services/            # Facade pattern implementation
│   └── persistence/         # Data storage layer
├── tests/                   # Test files
├── run.py                   # Application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd hbnb
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Development mode
```bash
python run.py
```

The application will start on `http://localhost:5000`

### API Documentation
Access the Swagger UI at: `http://localhost:5000/api/v1/`

## Testing

### Run all tests
```bash
python -m pytest tests/
```

### Run specific test file
```bash
python -m pytest tests/test_user_endpoints.py -v
```

## API Endpoints

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user

### Places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/` - Get all places
- `GET /api/v1/places/{place_id}` - Get place by ID
- `PUT /api/v1/places/{place_id}` - Update place

### Reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/` - Get all reviews
- `GET /api/v1/reviews/{review_id}` - Get review by ID
- `PUT /api/v1/reviews/{review_id}` - Update review
- `DELETE /api/v1/reviews/{review_id}` - Delete review
- `GET /api/v1/places/{place_id}/reviews` - Get all reviews for a place

### Amenities
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/` - Get all amenities
- `GET /api/v1/amenities/{amenity_id}` - Get amenity by ID
- `PUT /api/v1/amenities/{amenity_id}` - Update amenity

## Architecture

The application follows a layered architecture:
- **Presentation Layer**: RESTful API endpoints using Flask-RESTX
- **Business Logic Layer**: Core models and business rules
- **Service Layer**: Facade pattern for simplified access
- **Persistence Layer**: In-memory repository (to be replaced with database in Part 3)

## Contributing
Please read the contributing guidelines before submitting pull requests.

## License
This project is part of the Holberton School curriculum.
