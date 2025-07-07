"""User model class"""
from app.models.base_model import BaseModel
import re

class User(BaseModel):
    """User model representing a user in the system"""
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize User instance"""
        super().__init__()
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.places = []
    
    @staticmethod
    def _validate_name(name, field_name):
        """Validate name fields"""
        if not name or not name.strip():
            raise ValueError(f"{field_name} is required")
        name = name.strip()
        if len(name) > 50:
            raise ValueError(f"{field_name} must be 50 characters or less")
        return name
    
    @staticmethod
    def _validate_email(email):
        """Validate email format"""
        if not email:
            raise ValueError("Email is required")
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.lower()):
            raise ValueError("Invalid email format")
        return email.lower()
    
    def add_place(self, place):
        """Add a place to user's places"""
        if place not in self.places:
            self.places.append(place)
    
    def update(self, data):
        """Update user attributes with validation"""
        if 'first_name' in data:
            data['first_name'] = self._validate_name(data['first_name'], "First name")
        if 'last_name' in data:
            data['last_name'] = self._validate_name(data['last_name'], "Last name")
        if 'email' in data:
            data['email'] = self._validate_email(data['email'])
        super().update(data)
    
    def to_dict(self):
        """Convert user to dictionary"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return data