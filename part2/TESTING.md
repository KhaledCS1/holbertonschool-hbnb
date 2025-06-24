# HBnB Testing Guide

## Table of Contents
1. [Running Tests](#running-tests)
2. [Manual Testing with cURL](#manual-testing)
3. [API Documentation](#api-documentation)
4. [Test Coverage](#test-coverage)

## Running Tests

### Install Testing Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
# Using pytest
python -m pytest tests/ -v

# Using unittest
python -m unittest discover tests
```

### Run Specific Test File
```bash
# Test user endpoints
python -m pytest tests/test_user_endpoints.py -v

# Test models
python -m pytest tests/test_models.py -v
```

### Run with Coverage
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

## Manual Testing with cURL

### User Endpoints

#### Create User
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }'
```

#### Get All Users
```bash
curl -X GET http://localhost:5000/api/v1/users/
```

#### Get User by ID
```bash
curl -X GET http://localhost:5000/api/v1/users/{user_id}
```

#### Update User
```bash
curl -X PUT http://localhost:5000/api/v1/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com"
  }'
```

### Place Endpoints

#### Create Place
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beach House",
    "description": "Beautiful beach house",
    "price": 150.0,
    "latitude": 34.0522,
    "longitude": -118.2437,
    "owner_id": "{owner_user_id}"
  }'
```

#### Get Place with Details
```bash
curl -X GET http://localhost:5000/api/v1/places/{place_id}
```

### Review Endpoints

#### Create Review
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Amazing place!",
    "rating": 5,
    "user_id": "{user_id}",
    "place_id": "{place_id}"
  }'
```

#### Delete Review
```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/{review_id}
```

#### Get Reviews for a Place
```bash
curl -X GET http://localhost:5000/api/v1/places/{place_id}/reviews
```

### Amenity Endpoints

#### Create Amenity
```bash
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wi-Fi"
  }'
```

#### Get All Amenities
```bash
curl -X GET http://localhost:5000/api/v1/amenities/
```

## API Documentation

### Swagger UI
Access the interactive API documentation at:
```
http://localhost:5000/api/v1/
```

### Response Format

#### Success Response
```json
{
  "id": "uuid",
  "field1": "value1",
  "field2": "value2",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Error Response
```json
{
  "message": "Error description"
}
```

### Status Codes

| Code | Description | Usage |
|------|-------------|-------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | Resource not found |

## Test Coverage

### Current Test Coverage
- User endpoints: ✅ 100%
- Place endpoints: ✅ 100%
- Review endpoints: ✅ 100%
- Amenity endpoints: ✅ 100%
- Model validation: ✅ 100%

### Validation Tests

#### Email Validation
- ✅ Valid email format
- ✅ Invalid email format
- ✅ Empty email
- ✅ Email uniqueness

#### Price Validation
- ✅ Positive prices
- ✅ Negative prices rejected
- ✅ Zero price rejected

#### Coordinate Validation
- ✅ Valid latitude (-90 to 90)
- ✅ Valid longitude (-180 to 180)
- ✅ Out of range values rejected

#### Rating Validation
- ✅ Valid ratings (1-5)
- ✅ Out of range ratings rejected
- ✅ Non-integer ratings rejected

### Edge Cases Tested
- Empty strings
- Missing required fields
- Maximum length validation
- Non-existent resources
- Duplicate resources

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 5000
   lsof -i :5000
   kill -9 <PID>
   ```

2. **Import Errors**
   ```bash
   # Make sure you're in the project root
   cd hbnb
   python -m pytest tests/
   ```

3. **Database State Between Tests**
   - Tests use in-memory storage
   - Each test starts with clean state
   - No persistence between test runs
