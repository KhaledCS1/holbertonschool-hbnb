"""Tests for user endpoints"""
import unittest
import json
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    """Test cases for user endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}
    
    def test_create_user_success(self):
        """Test successful user creation"""
        # Prepare test data
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        
        # Send request
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        
        # Check response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        user_data = {
            "first_name": "Invalid",
            "last_name": "Email",
            "email": "not-an-email"
        }
        
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_create_user_missing_fields(self):
        """Test user creation with missing required fields"""
        user_data = {
            "first_name": "John"
            # Missing last_name and email
        }
        
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_users(self):
        """Test retrieving all users"""
        # First create a user
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        }
        self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        
        # Get all users
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
    
    def test_get_user_by_id(self):
        """Test retrieving a specific user"""
        # Create a user
        user_data = {
            "first_name": "Specific",
            "last_name": "User",
            "email": "specific@example.com"
        }
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['email'], 'specific@example.com')
    
    def test_get_nonexistent_user(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/invalid-id-12345')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_update_user(self):
        """Test updating user information"""
        # Create a user
        user_data = {
            "first_name": "Original",
            "last_name": "Name",
            "email": "original@example.com"
        }
        create_response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        created_user = json.loads(create_response.data)
        user_id = created_user['id']
        
        # Update the user
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@example.com"
        }
        response = self.client.put(
            f'/api/v1/users/{user_id}',
            data=json.dumps(update_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify the update
        get_response = self.client.get(f'/api/v1/users/{user_id}')
        data = json.loads(get_response.data)
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['email'], 'updated@example.com')
    
    def test_email_uniqueness(self):
        """Test that email must be unique"""
        user_data = {
            "first_name": "First",
            "last_name": "User",
            "email": "duplicate@example.com"
        }
        
        # Create first user
        response1 = self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        self.assertEqual(response1.status_code, 201)
        
        # Try to create second user with same email
        user_data['first_name'] = "Second"
        response2 = self.client.post(
            '/api/v1/users/',
            data=json.dumps(user_data),
            headers=self.headers
        )
        
        self.assertEqual(response2.status_code, 400)
        data = json.loads(response2.data)
        self.assertIn('already registered', data['message'])


if __name__ == '__main__':
    unittest.main()
