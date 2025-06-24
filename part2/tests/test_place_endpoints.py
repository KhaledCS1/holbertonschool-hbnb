"""Tests for place endpoints"""
import unittest
import json
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for place endpoints"""
    
    def setUp(self):
        """Set up test client and create test owner"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.headers = {'Content-Type': 'application/json'}
        
        # Create a test owner
        owner_data = {
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner@example.com"
        }
        response = self.client.post(
            '/api/v1/users/',
            data=json.dumps(owner_data),
            headers=self.headers
        )
        self.owner_id = json.loads(response.data)['id']
    
    def test_create_place_success(self):
        """Test successful place creation"""
        place_data = {
            "title": "Beautiful Beach House",
            "description": "A lovely house by the beach",
            "price": 150.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": self.owner_id
        }
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beautiful Beach House')
        self.assertEqual(data['price'], 150.0)
    
    def test_create_place_invalid_price(self):
        """Test place creation with invalid price"""
        place_data = {
            "title": "Test Place",
            "description": "Test description",
            "price": -50.0,  # Negative price
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": self.owner_id
        }
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('positive', data['message'].lower())
    
    def test_create_place_invalid_coordinates(self):
        """Test place creation with invalid coordinates"""
        # Test invalid latitude
        place_data = {
            "title": "Test Place",
            "description": "Test",
            "price": 100.0,
            "latitude": 95.0,  # Out of range
            "longitude": -118.2437,
            "owner_id": self.owner_id
        }
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('latitude', data['message'].lower())
        
        # Test invalid longitude
        place_data['latitude'] = 34.0522
        place_data['longitude'] = 200.0  # Out of range
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('longitude', data['message'].lower())
    
    def test_create_place_nonexistent_owner(self):
        """Test place creation with non-existent owner"""
        place_data = {
            "title": "Test Place",
            "description": "Test",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": "invalid-owner-id"
        }
        
        response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('not found', data['message'].lower())
    
    def test_get_place_with_details(self):
        """Test retrieving place with all details"""
        # Create a place
        place_data = {
            "title": "Detailed Place",
            "description": "With all details",
            "price": 200.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner_id
        }
        
        create_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            headers=self.headers
        )
        place_id = json.loads(create_response.data)['id']
        
        # Get the place
        response = self.client.get(f'/api/v1/places/{place_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check all details are included
        self.assertEqual(data['id'], place_id)
        self.assertIn('owner', data)
        self.assertEqual(data['owner']['id'], self.owner_id)
        self.assertIn('amenities', data)
        self.assertIsInstance(data['amenities'], list)
        self.assertIn('reviews', data)
        self.assertIsInstance(data['reviews'], list)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
    
    def test_update_place(self):
        """Test updating place information"""
        # Create a place
        place_data = {
            "title": "Original Title",
            "description": "Original description",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner_id
        }
        
        create_response = self.client.post(
            '/api/v1/places/',
            data=json.dumps(place_data),
            headers=self.headers
        )
        place_id = json.loads(create_response.data)['id']
        
        # Update the place
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.owner_id  # This should be ignored
        }
        
        response = self.client.put(
            f'/api/v1/places/{place_id}',
            data=json.dumps(update_data),
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify the update
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        data = json.loads(get_response.data)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['price'], 150.0)


if __name__ == '__main__':
    unittest.main()
