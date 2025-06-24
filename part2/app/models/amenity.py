"""Amenity model class"""
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity model representing a place amenity"""
    
    def __init__(self, name):
        """Initialize Amenity instance
        
        Args:
            name (str): Name of the amenity
        """
        super().__init__()
        
        # Validate and set name
        self.name = self._validate_name(name)
    
    @staticmethod
    def _validate_name(name):
        """Validate amenity name"""
        if not name or not name.strip():
            raise ValueError("Amenity name is required")
        
        name = name.strip()
        if len(name) > 50:
            raise ValueError("Amenity name must be 50 characters or less")
        
        return name
    
    def update(self, data):
        """Update amenity attributes with validation"""
        # Validate data before updating
        if 'name' in data:
            data['name'] = self._validate_name(data['name'])
        
        super().update(data)
    
    def to_dict(self):
        """Convert amenity to dictionary"""
        data = super().to_dict()
        data.update({
            'name': self.name
        })
        return data
