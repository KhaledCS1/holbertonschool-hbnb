# Class Diagram - Explanatory Notes

## Entity Descriptions

### BaseModel (Abstract Class)
**Role**: Abstract base class that provides common attributes and methods for all entities.

**Key Attributes**:
- `id`: Unique identifier (UUID4) for each entity instance
- `created_at`: Timestamp of when the entity was created
- `updated_at`: Timestamp of when the entity was last updated

**Key Methods**:
- `save()`: Persists the entity to the database
- `update()`: Updates the entity in the database
- `delete()`: Removes the entity from the database

### User Entity
**Role**: Represents a user in the system who can own places and write reviews.

**Key Attributes**:
- `first_name`: User's first name
- `last_name`: User's last name
- `email`: User's email address (unique identifier for authentication)
- `password`: User's encrypted password
- `is_admin`: Boolean flag indicating if the user has administrative privileges
- `places`: List of places owned by the user
- `reviews`: List of reviews written by the user

**Key Methods**:
- `register()`: Creates a new user account
- `authenticate()`: Validates user credentials
- `update_profile()`: Updates user information
- `delete_account()`: Removes user account
- `get_places()`: Retrieves all places owned by the user
- `get_reviews()`: Retrieves all reviews written by the user

### Place Entity
**Role**: Represents a property that can be listed in the application.

**Key Attributes**:
- `title`: Name of the place
- `description`: Detailed description of the place
- `price`: Price per night
- `latitude`: Geographic latitude coordinate
- `longitude`: Geographic longitude coordinate
- `owner`: Reference to the User who owns the place
- `reviews`: List of reviews for the place
- `amenities`: List of amenities available at the place

**Key Methods**:
- `create()`: Creates a new place listing
- `update_details()`: Updates place information
- `delete()`: Removes place from listings
- `add_amenity(amenity)`: Associates an amenity with the place
- `remove_amenity(amenity)`: Removes an amenity association
- `get_reviews()`: Retrieves all reviews for the place
- `calculate_average_rating()`: Computes the average rating from all reviews

### Review Entity
**Role**: Represents a review written by a user for a place.

**Key Attributes**:
- `rating`: Numerical rating (1-5)
- `comment`: Text review comment
- `user`: Reference to the User who wrote the review
- `place`: Reference to the Place being reviewed

**Key Methods**:
- `create()`: Creates a new review
- `update()`: Updates review content
- `delete()`: Removes the review
- `validate_rating()`: Ensures rating is within valid range (1-5)

### Amenity Entity
**Role**: Represents amenities that can be associated with places.

**Key Attributes**:
- `name`: Name of the amenity (e.g., "WiFi", "Pool")
- `description`: Detailed description of the amenity
- `places`: List of places that have this amenity

**Key Methods**:
- `create()`: Creates a new amenity
- `update()`: Updates amenity information
- `delete()`: Removes the amenity
- `get_places()`: Retrieves all places that have this amenity

## Relationships

### Inheritance Relationships
- All entities (User, Place, Review, Amenity) inherit from BaseModel
- This ensures consistent behavior for common operations (save, update, delete)
- All entities have unique IDs and timestamps

### Association Relationships

1. **User owns Place** (1 to 0..*)
   - One user can own zero or more places
   - Each place must have exactly one owner
   - This is a composition relationship - if a user is deleted, their places should be handled appropriately

2. **User writes Review** (1 to 0..*)
   - One user can write zero or more reviews
   - Each review must be written by exactly one user

3. **Place has Review** (1 to 0..*)
   - One place can have zero or more reviews
   - Each review must be associated with exactly one place

4. **Place has Amenity** (0..* to 0..*)
   - A place can have zero or more amenities
   - An amenity can be associated with zero or more places
   - This is a many-to-many relationship requiring a junction table in the database

## Business Logic Considerations

1. **User Deletion**: When a user is deleted, their places and reviews must be handled according to business rules (cascade delete or reassignment)

2. **Place Deletion**: When a place is deleted, all associated reviews should be deleted

3. **Review Validation**: Reviews must validate that the rating is between 1 and 5

4. **Unique Constraints**: 
   - User email must be unique
   - Amenity name should be unique

5. **Authentication**: Password should be hashed before storage

6. **Authorization**: Only place owners should be able to update or delete their places
