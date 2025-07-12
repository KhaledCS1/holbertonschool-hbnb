"""
Suhail Al-aboud <10675@holbertonstudents.com>
Facade pattern implementation for simplified access to business logic
"""
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """Facade class for managing all application operations."""

    def __init__(self):
        """Initialize repositories for all entities using SQLAlchemy."""
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ========== User Management ==========

    def create_user(self, user_data):
        """Create a new user."""
        existing_user = self.get_user_by_email(user_data.get("email", ""))
        if existing_user:
            raise ValueError("Email already registered")

        if "password" not in user_data:
            raise ValueError("Password is required")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email (case‑insensitive)."""
        return self.user_repo.get_by_attribute("email", email.lower())

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.get_user(user_id)
        if not user:
            return None

        if "email" in user_data and user_data["email"].lower() != user.email:
            existing = self.get_user_by_email(user_data["email"])
            if existing:
                raise ValueError("Email already registered")

        user.update(user_data)
        return user

    # ========== Place Management ==========

    def create_place(self, place_data):
        """Create a new place."""
        owner_id = place_data.pop("owner_id", None)
        if not owner_id:
            raise ValueError("Owner ID is required")

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(**place_data, owner=owner)
        self.place_repo.add(place)
        owner.add_place(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.get_place(place_id)
        if not place:
            return None

        place_data.pop("owner_id", None)
        place_data.pop("owner", None)

        place.update(place_data)
        return place

    # ========== Review Management ==========

    def create_review(self, review_data):
        """Create a new review."""
        user_id = review_data.pop("user_id", None)
        place_id = review_data.pop("place_id", None)

        if not user_id or not place_id:
            raise ValueError("User ID and Place ID are required")

        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        review = Review(**review_data, place=place, user=user)
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place."""
        place = self.get_place(place_id)
        if place:
            return place.reviews
        return []

    def update_review(self, review_id, review_data):
        """Update a review."""
        review = self.get_review(review_id)
        if not review:
            return None

        review.update(review_data)
        return review

    def delete_review(self, review_id):
        """Delete a review."""
        review = self.get_review(review_id)
        if not review:
            return False

        if review.place:
            review.place.reviews.remove(review)

        self.review_repo.delete(review_id)
        return True

    # ========== Amenity Management ==========

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        amenity.update(amenity_data)
        return amenity
