# HBnB Evolution - Part 1: Technical Documentation

## Team Members
- Suhail Alaboud
- Khaled Almimoni
- Abrar Almukhlifi

## Task 0: High-Level Package Diagram

This document contains the high-level package diagram for the HBnB Evolution application, illustrating the three-layer architecture and communication via the facade pattern.

## Architecture Overview

The HBnB Evolution application follows a three-layer architecture:

1. **Presentation Layer**: Handles API endpoints and services
2. **Business Logic Layer**: Contains core models and business rules
3. **Persistence Layer**: Manages data storage and retrieval

## Package Diagram

The package diagram shows the organization of the application components and their relationships. The facade pattern is used to simplify communication between layers.

### Key Components

#### Presentation Layer
- **API Endpoints**: RESTful routes for all entity management
  - User Management API
  - Place Management API
  - Review Management API
  - Amenity Management API
- **Services**: Handle request processing and response formatting

#### Facade Pattern
- Provides a unified interface for all business operations
- Simplifies interaction between presentation and business logic layers
- Centralizes error handling and validation

#### Business Logic Layer
- **User Model**: Manages user-related operations
- **Place Model**: Handles place management and amenity associations
- **Review Model**: Manages reviews and ratings
- **Amenity Model**: Handles amenity operations

#### Persistence Layer
- **Repositories**: Implement data access patterns for each entity
- **Database**: Stores all application data

## Communication Flow

1. Client requests are received by the Presentation Layer
2. Services process requests and call the Facade Interface
3. Facade delegates operations to appropriate models in Business Logic Layer
4. Models use repositories in Persistence Layer for data operations
5. Responses flow back through the same path

## Benefits of This Architecture

- **Separation of Concerns**: Each layer has distinct responsibilities
- **Maintainability**: Changes in one layer don't affect others
- **Testability**: Each layer can be tested independently
- **Scalability**: Layers can be scaled independently
- **Flexibility**: Easy to swap implementations

## Diagrams

- See `package_diagram.mmd` for the detailed Mermaid.js diagram
- See `uml_package_diagram.mmd` for the UML package diagram
- See `architecture_notes.md` for detailed explanations

## Task 1: Detailed Class Diagram for Business Logic Layer

The class diagram for the Business Logic Layer shows the detailed structure of the core entities and their relationships.

### Key Entities
- **BaseModel**: Abstract base class providing common attributes (id, created_at, updated_at)
- **User**: Manages user accounts and authentication
- **Place**: Represents properties that can be listed
- **Review**: Handles user reviews for places
- **Amenity**: Manages amenities that can be associated with places

### Relationships
- Inheritance: All entities inherit from BaseModel
- User owns Place (1 to many)
- User writes Review (1 to many)
- Place has Review (1 to many)
- Place has Amenity (many to many)

See `class_diagram.mmd` for the detailed UML class diagram and `class_diagram_notes.md` for comprehensive explanations.

## Task 2: Sequence Diagrams for API Calls

Four sequence diagrams have been created to illustrate the interaction flow between layers for key API operations:

1. **User Registration**: Shows the process of creating a new user account
2. **Place Creation**: Demonstrates how users create property listings
3. **Review Submission**: Illustrates the review creation process
4. **Fetching Places**: Shows how filtered place lists are retrieved

Each diagram depicts the communication between:
- Presentation Layer (API & Services)
- Business Logic Layer (Models) via Facade Pattern
- Persistence Layer (Repositories & Database)

See the following files:
- `user_registration_sequence.mmd` - User registration flow
- `place_creation_sequence.mmd` - Place creation flow
- `review_submission_sequence.mmd` - Review submission flow
- `fetch_places_sequence.mmd` - Places retrieval flow
- `sequence_diagrams_notes.md` - Detailed explanations for all sequences

## Task 3: Documentation Compilation

A comprehensive technical document has been created that combines all diagrams and explanatory notes from previous tasks into a single, cohesive reference document.

### Document Contents:
1. **Introduction**: Project overview and document purpose
2. **High-Level Architecture**: Package diagrams and layer explanations
3. **Business Logic Layer**: Class diagrams and entity specifications
4. **API Interaction Flow**: Sequence diagrams for all API operations
5. **Implementation Guidelines**: Best practices and next steps

The complete technical documentation serves as the definitive blueprint for the HBnB Evolution project implementation.

See `technical_documentation.md` for the complete compiled documentation.
