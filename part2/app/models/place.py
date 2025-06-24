"""Place model class"""
from app.models.base_model import BaseModel

class Place(BaseModel):
    """Place model representing a rental property"""
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialize Place instance
        
        Args:
            title (str): Title of the place
            description (str): Description of the place
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): User who owns the place
        """
        super().__init__()
        
        # Validate and set attributes
        self.title = self._validate_title(title)
        self.description = description if description else ""
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = owner
        
        # Lists for relationships
        self.reviews = []
        self.amenities = []
    
    @staticmethod
    def _validate_title(title):
        """Validate place title"""
        if not title or not title.strip():
            raise ValueError("Title is required")
        
        title = title.strip()
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")
        
        return title
    
    @staticmethod
    def _validate_price(price):
        """Validate price"""
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        
        if price <= 0:
            raise ValueError("Price must be a positive number")
        
        return float(price)
    
    @staticmethod
    def _validate_latitude(latitude):
        """Validate latitude coordinate"""
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        
        return float(latitude)
    
    @staticmethod
    def _validate_longitude(longitude):
        """Validate longitude coordinate"""
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        return float(longitude)
    
    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)
    
    def add_amenity(self, amenity):
        """Add an amenity to the place"""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        """Remove an amenity from the place"""
        if amenity in self.amenities:
            self.amenities.remove(amenity)
    
    def update(self, data):
        """Update place attributes with validation"""
        # Validate data before updating
        if 'title' in data:
            data['title'] = self._validate_title(data['title'])
        if 'price' in data:
            data['price'] = self._validate_price(data['price'])
        if 'latitude' in data:
            data['latitude'] = self._validate_latitude(data['latitude'])
        if 'longitude' in data:
            data['longitude'] = self._validate_longitude(data['longitude'])
        
        super().update(data)
    
    def to_dict(self):
        """Convert place to dictionary"""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if self.owner else None
        })
        return data
