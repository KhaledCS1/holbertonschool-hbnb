"""Review model class"""
from app.models.base_model import BaseModel

class Review(BaseModel):
    """Review model representing a place review"""
    
    def __init__(self, text, rating, place, user):
        """Initialize Review instance"""
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = place
        self.user = user
    
    @staticmethod
    def _validate_text(text):
        """Validate review text"""
        if not text or not text.strip():
            raise ValueError("Review text is required")
        return text.strip()
    
    @staticmethod
    def _validate_rating(rating):
        """Validate rating"""
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def update(self, data):
        """Update review attributes with validation"""
        if 'text' in data:
            data['text'] = self._validate_text(data['text'])
        if 'rating' in data:
            data['rating'] = self._validate_rating(data['rating'])
        
        # Don't allow updating place or user
        data.pop('place', None)
        data.pop('user', None)
        data.pop('place_id', None)
        data.pop('user_id', None)
        
        super().update(data)
    
    def to_dict(self):
        """Convert review to dictionary"""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id if self.user else None,
            'place_id': self.place.id if self.place else None
        })
        return data