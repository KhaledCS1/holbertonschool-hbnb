"""Base model class with common attributes"""
import uuid
from datetime import datetime

class BaseModel:
    """Base class for all models"""
    
    def __init__(self):
        """Initialize base attributes"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'updated_at']:
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Convert object to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }