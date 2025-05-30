# Sequence Diagrams - Explanatory Notes

## 1. User Registration Sequence

### Purpose
Illustrates the process of creating a new user account in the HBnB application.

### Key Steps
1. **Client Request**: User submits registration data via POST request
2. **Input Validation**: API layer validates the request format
3. **Service Processing**: UserService validates business rules
4. **User Creation**: Facade coordinates with User Model to create new user
5. **Password Security**: User Model hashes the password before storage
6. **Data Persistence**: User Repository saves the user to database
7. **Response**: Success confirmation returned to client

### Flow Highlights
- Email uniqueness is validated before creating the user
- Password is hashed for security before database storage
- User object is created with unique ID and timestamps
- HTTP 201 status indicates successful resource creation

## 2. Place Creation Sequence

### Purpose
Shows how a user creates a new place listing in the system.

### Key Steps
1. **Authentication**: Request includes user ID for ownership
2. **User Verification**: System verifies the user exists
3. **Place Validation**: Coordinates and other place data are validated
4. **Owner Assignment**: Place is linked to the creating user
5. **Database Storage**: Place is saved with all attributes
6. **Response Generation**: New place data returned to client

### Flow Highlights
- User must exist before place can be created
- Place ownership is established during creation
- Coordinates validation ensures valid location data
- Place receives unique ID and creation timestamp

## 3. Review Submission Sequence

### Purpose
Demonstrates the process of a user submitting a review for a place.

### Key Steps
1. **Target Identification**: Place ID provided in the request URL
2. **Place Verification**: System confirms place exists
3. **User Verification**: System confirms reviewing user exists
4. **Rating Validation**: Review rating checked for valid range (1-5)
5. **Association Creation**: Review linked to both user and place
6. **Database Storage**: Review saved with all relationships
7. **Response**: Created review returned to client

### Flow Highlights
- Both place and user must exist before review creation
- Rating validation ensures data quality
- Review is associated with both user and place
- Prevents duplicate reviews through business logic

## 4. Fetching Places List Sequence

### Purpose
Shows how the system retrieves and returns a filtered list of places.

### Key Steps
1. **Criteria Reception**: GET request includes filter parameters
2. **Criteria Validation**: Service validates the search criteria
3. **Database Query**: Repository executes filtered query
4. **Amenities Loading**: For each place, associated amenities are loaded
5. **Data Assembly**: Places combined with their amenities
6. **Response Formatting**: Data formatted for client consumption
7. **Response Delivery**: Complete place list returned

### Flow Highlights
- Supports various filter criteria (location, price, amenities)
- Efficient loading of related amenities data
- Pagination can be implemented at repository level
- Response includes complete place information

## Layer Interactions

### Presentation Layer (API & Services)
- Handles HTTP requests and responses
- Validates input format and parameters
- Manages response formatting
- Implements authentication checks

### Business Logic Layer (Models)
- Enforces business rules and constraints
- Manages entity relationships
- Handles data validation
- Implements domain-specific logic

### Persistence Layer (Repositories & Database)
- Executes database queries
- Manages transactions
- Handles data mapping
- Optimizes query performance

## Common Patterns

1. **Validation Chain**: Input validated at multiple layers
2. **Facade Pattern**: Simplifies complex operations
3. **Repository Pattern**: Abstracts database operations
4. **Error Propagation**: Errors bubble up through layers
5. **Response Formatting**: Data transformed for client needs
