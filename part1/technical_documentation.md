# HBnB Evolution - Technical Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [High-Level Architecture](#high-level-architecture)
3. [Business Logic Layer](#business-logic-layer)
4. [API Interaction Flow](#api-interaction-flow)
5. [Conclusion](#conclusion)

---

## 1. Introduction

### Project Overview
HBnB Evolution is a simplified version of an AirBnB-like application designed to demonstrate modern software architecture principles and best practices. This web-based platform enables users to list properties, browse accommodations, and share reviews, creating a comprehensive property rental marketplace.

### Document Purpose
This technical documentation serves as the definitive blueprint for the HBnB Evolution project. It provides detailed architectural diagrams, design specifications, and implementation guidelines that will guide developers through all phases of the project lifecycle. The document ensures consistency, clarity, and alignment among all team members working on the project.

### Document Scope
This document covers:
- System architecture using a three-layer design pattern
- Detailed specifications of the Business Logic layer entities
- API interaction flows for core functionality
- Design decisions and their rationale
- Implementation guidelines and best practices

---

## 2. High-Level Architecture

### Overview
The HBnB Evolution application follows a three-layer architecture pattern, ensuring separation of concerns, maintainability, and scalability. The architecture implements the Facade pattern to manage communication between layers effectively.

### Package Diagram

![Package Diagram](package_diagram.mmd)

### Architectural Layers

#### 2.1 Presentation Layer
**Purpose**: Serves as the interface between users and the application system.

**Components**:
- **API Endpoints**: RESTful routes handling HTTP requests and responses
- **Services**: Business logic orchestration and request processing

**Responsibilities**:
- HTTP request/response handling
- Input validation and sanitization
- Authentication and authorization
- Response formatting and error handling

#### 2.2 Business Logic Layer
**Purpose**: Contains the core application logic and business rules.

**Components**:
- **User Model**: User account management and authentication
- **Place Model**: Property listing management
- **Review Model**: Review and rating management
- **Amenity Model**: Property amenity management

**Responsibilities**:
- Business rule enforcement
- Data validation and integrity
- Entity relationship management
- Complex operation orchestration

#### 2.3 Persistence Layer
**Purpose**: Manages all data storage and retrieval operations.

**Components**:
- **Repositories**: Data access objects for each entity
- **Database**: Relational database for persistent storage

**Responsibilities**:
- CRUD operations
- Query optimization
- Transaction management
- Data persistence and retrieval

### Facade Pattern Implementation

The Facade pattern provides a unified interface between the Presentation and Business Logic layers, offering several benefits:

1. **Simplified Interface**: Single entry point for all business operations
2. **Loose Coupling**: Reduces dependencies between layers
3. **Centralized Error Handling**: Consistent error management across operations
4. **Enhanced Testability**: Easier to mock and test individual components

**Key Operations**:
- `userOperations()`: Manages all user-related operations
- `placeOperations()`: Handles place management functions
- `reviewOperations()`: Controls review-related operations
- `amenityOperations()`: Manages amenity operations

---

## 3. Business Logic Layer

### Overview
The Business Logic layer implements the core domain models and business rules of the HBnB Evolution application. All entities inherit from a common BaseModel class, ensuring consistent behavior across the system.

### Class Diagram

![Class Diagram](class_diagram.mmd)

### Entity Specifications

#### 3.1 BaseModel (Abstract Class)
**Purpose**: Provides common attributes and methods for all entities.

**Attributes**:
- `id` (String): Unique identifier (UUID4)
- `created_at` (DateTime): Entity creation timestamp
- `updated_at` (DateTime): Last modification timestamp

**Methods**:
- `save()`: Persists entity to database
- `update()`: Updates entity in database
- `delete()`: Removes entity from database

#### 3.2 User Entity
**Purpose**: Represents system users who can own places and write reviews.

**Attributes**:
- `first_name` (String): User's first name
- `last_name` (String): User's last name
- `email` (String): Unique email address
- `password` (String): Encrypted password
- `is_admin` (Boolean): Administrative privileges flag
- `places` (List<Place>): Owned places
- `reviews` (List<Review>): Written reviews

**Methods**:
- `register()`: Creates new user account
- `authenticate()`: Validates credentials
- `update_profile()`: Updates user information
- `delete_account()`: Removes user account
- `get_places()`: Retrieves owned places
- `get_reviews()`: Retrieves written reviews

#### 3.3 Place Entity
**Purpose**: Represents properties available for rental.

**Attributes**:
- `title` (String): Property name
- `description` (String): Detailed description
- `price` (Float): Price per night
- `latitude` (Float): Geographic latitude
- `longitude` (Float): Geographic longitude
- `owner` (User): Property owner reference
- `reviews` (List<Review>): Property reviews
- `amenities` (List<Amenity>): Available amenities

**Methods**:
- `create()`: Creates new listing
- `update_details()`: Updates property information
- `delete()`: Removes listing
- `add_amenity()`: Associates amenity
- `remove_amenity()`: Disassociates amenity
- `get_reviews()`: Retrieves property reviews
- `calculate_average_rating()`: Computes average rating

#### 3.4 Review Entity
**Purpose**: Represents user reviews for places.

**Attributes**:
- `rating` (Integer): Numerical rating (1-5)
- `comment` (String): Review text
- `user` (User): Review author
- `place` (Place): Reviewed property

**Methods**:
- `create()`: Creates new review
- `update()`: Updates review content
- `delete()`: Removes review
- `validate_rating()`: Ensures valid rating range

#### 3.5 Amenity Entity
**Purpose**: Represents amenities available at properties.

**Attributes**:
- `name` (String): Amenity name
- `description` (String): Amenity description
- `places` (List<Place>): Associated properties

**Methods**:
- `create()`: Creates new amenity
- `update()`: Updates amenity information
- `delete()`: Removes amenity
- `get_places()`: Retrieves associated places

### Entity Relationships

1. **Inheritance**: All entities inherit from BaseModel
2. **User-Place**: One-to-many (User owns multiple Places)
3. **User-Review**: One-to-many (User writes multiple Reviews)
4. **Place-Review**: One-to-many (Place has multiple Reviews)
5. **Place-Amenity**: Many-to-many (Places can have multiple Amenities)

---

## 4. API Interaction Flow

### Overview
The sequence diagrams below illustrate the interaction flow between system layers for core API operations. Each diagram shows the step-by-step process from client request to response.

### 4.1 User Registration Flow

![User Registration Sequence](user_registration_sequence.mmd)

**Purpose**: Creates a new user account in the system.

**Key Steps**:
1. Client sends POST request with user data
2. API layer validates request format
3. Service layer checks business rules
4. Facade coordinates user creation
5. Password is hashed for security
6. User is persisted to database
7. Success response returned to client

**Critical Validations**:
- Email uniqueness check
- Password strength requirements
- Required field validation

### 4.2 Place Creation Flow

![Place Creation Sequence](place_creation_sequence.mmd)

**Purpose**: Allows users to create new property listings.

**Key Steps**:
1. Client sends POST request with place data
2. User authentication verified
3. Place data validated
4. Owner relationship established
5. Place persisted to database
6. Created place returned to client

**Critical Validations**:
- User authorization check
- Coordinate validation
- Price range validation

### 4.3 Review Submission Flow

![Review Submission Sequence](review_submission_sequence.mmd)

**Purpose**: Enables users to submit reviews for places.

**Key Steps**:
1. Client sends POST request with review data
2. Place existence verified
3. User authorization confirmed
4. Rating validated (1-5 range)
5. Review associations created
6. Review persisted to database
7. Success response returned

**Critical Validations**:
- Place must exist
- User must be authenticated
- Rating must be within valid range
- Duplicate review prevention

### 4.4 Fetching Places Flow

![Fetching Places Sequence](fetch_places_sequence.mmd)

**Purpose**: Retrieves filtered list of available places.

**Key Steps**:
1. Client sends GET request with filters
2. Filter criteria validated
3. Database query executed
4. Associated amenities loaded
5. Response formatted
6. Place list returned to client

**Supported Filters**:
- Location-based filtering
- Price range filtering
- Amenity filtering
- Availability filtering

### Common Interaction Patterns

1. **Authentication Check**: All protected endpoints verify user authentication
2. **Input Validation**: Multi-layer validation ensures data integrity
3. **Error Handling**: Consistent error responses across all endpoints
4. **Response Formatting**: Standardized response structure
5. **Database Transactions**: Atomic operations ensure data consistency

---

## 5. Conclusion

### Implementation Guidelines

1. **Follow Layer Boundaries**: Maintain strict separation between layers
2. **Use Dependency Injection**: Facilitate testing and flexibility
3. **Implement Error Handling**: Comprehensive error management at each layer
4. **Maintain Documentation**: Keep technical documentation updated
5. **Write Tests**: Comprehensive test coverage for all components

### Next Steps

1. **Environment Setup**: Configure development environment
2. **Database Schema**: Implement database tables and relationships
3. **API Implementation**: Develop RESTful endpoints
4. **Business Logic**: Implement models and business rules
5. **Testing**: Create comprehensive test suite
6. **Deployment**: Prepare production deployment

### Design Principles Applied

- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **DRY (Don't Repeat Yourself)**: Code reusability through inheritance and composition
- **KISS (Keep It Simple, Stupid)**: Simple, maintainable solutions
- **YAGNI (You Aren't Gonna Need It)**: Focus on current requirements

### Document Maintenance

This technical document should be treated as a living document and updated whenever:
- New features are added
- Architecture changes are made
- Design decisions are modified
- Implementation details change

Regular reviews ensure the documentation remains accurate and valuable throughout the project lifecycle.

---

**Document Version**: 1.0  
**Last Updated**: [Current Date]  
**Authors**: 
- Suhail Alaboud
- Khaled Almimoni
- Abrar Almukhlifi
