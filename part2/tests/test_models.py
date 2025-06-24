"""Tests for model classes"""
import unittest
from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestUserModel(unittest.TestCase):
    """Test cases for User model"""
    
    def test_user_creation(self):
        """Test creating a user with valid data"""
        user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)
        self.assertIsNotNone(user.id)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)
    
    def test_user_email_validation(self):
        """Test email validation"""
        # Invalid email
        with self.assertRaises(ValueError):
            User(
                first_name="Test",
                last_name="User",
                email="invalid-email"
            )
        
        # Empty email
        with self.assertRaises(ValueError):
            User(
                first_name="Test",
                last_name="User",
                email=""
            )
    
    def test_user_name_validation(self):
        """Test name validation"""
        # Empty first name
        with self.assertRaises(ValueError):
            User(
                first_name="",
                last_name="User",
                email="test@example.com"
            )
        
        # Long first name
        with self.assertRaises(ValueError):
            User(
                first_name="A" * 51,
                last_name="User",
                email="test@example.com"
            )


class TestPlaceModel(unittest.TestCase):
    """Test cases for Place model"""
    
    def setUp(self):
        """Create a test owner"""
        self.owner = User(
            first_name="Owner",
            last_name="User",
            email="owner@example.com"
        )
    
    def test_place_creation(self):
        """Test creating a place with valid data"""
        place = Place(
            title="Nice Place",
            description="A very nice place",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.owner
        )
        
        self.assertEqual(place.title, "Nice Place")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.owner, self.owner)
        self.assertIsNotNone(place.id)
    
    def test_place_price_validation(self):
        """Test price validation"""
        # Negative price
        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=-50.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner=self.owner
            )
        
        # Zero price
        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=0,
                latitude=40.7128,
                longitude=-74.0060,
                owner=self.owner
            )
    
    def test_place_coordinate_validation(self):
        """Test coordinate validation"""
        # Invalid latitude
        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=100.0,
                latitude=95.0,
                longitude=-74.0060,
                owner=self.owner
            )
        
        # Invalid longitude
        with self.assertRaises(ValueError):
            Place(
                title="Test",
                description="Test",
                price=100.0,
                latitude=40.7128,
                longitude=200.0,
                owner=self.owner
            )


class TestReviewModel(unittest.TestCase):
    """Test cases for Review model"""
    
    def setUp(self):
        """Create test user and place"""
        self.user = User(
            first_name="Reviewer",
            last_name="User",
            email="reviewer@example.com"
        )
        self.owner = User(
            first_name="Owner",
            last_name="User",
            email="owner@example.com"
        )
        self.place = Place(
            title="Test Place",
            description="Test",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=self.owner
        )
    
    def test_review_creation(self):
        """Test creating a review with valid data"""
        review = Review(
            text="Great place!",
            rating=5,
            place=self.place,
            user=self.user
        )
        
        self.assertEqual(review.text, "Great place!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)
    
    def test_review_rating_validation(self):
        """Test rating validation"""
        # Rating too low
        with self.assertRaises(ValueError):
            Review(
                text="Test",
                rating=0,
                place=self.place,
                user=self.user
            )
        
        # Rating too high
        with self.assertRaises(ValueError):
            Review(
                text="Test",
                rating=6,
                place=self.place,
                user=self.user
            )
        
        # Non-integer rating
        with self.assertRaises(ValueError):
            Review(
                text="Test",
                rating=3.5,
                place=self.place,
                user=self.user
            )


class TestAmenityModel(unittest.TestCase):
    """Test cases for Amenity model"""
    
    def test_amenity_creation(self):
        """Test creating an amenity with valid data"""
        amenity = Amenity(name="Wi-Fi")
        
        self.assertEqual(amenity.name, "Wi-Fi")
        self.assertIsNotNone(amenity.id)
    
    def test_amenity_name_validation(self):
        """Test name validation"""
        # Empty name
        with self.assertRaises(ValueError):
            Amenity(name="")
        
        # Long name
        with self.assertRaises(ValueError):
            Amenity(name="A" * 51)


if __name__ == '__main__':
    unittest.main()
