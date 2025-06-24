"""Base model class with common attributes and methods"""
import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models with common attributes"""
    
    def __init__(self):
        """Initialize base attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        # Update only allowed attributes (exclude id, created_at, updated_at)
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
