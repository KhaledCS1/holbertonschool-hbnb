erDiagram

    USERS {
        CHAR(36) id PK
        VARCHAR  first_name
        VARCHAR  last_name
        VARCHAR  email "UNIQUE"
        VARCHAR  password
        BOOLEAN  is_admin
        DATETIME created_at
        DATETIME updated_at
    }

    PLACES {
        CHAR(36) id PK
        VARCHAR  title
        TEXT     description
        DECIMAL  price
        FLOAT    latitude
        FLOAT    longitude
        CHAR(36) owner_id FK
        DATETIME created_at
        DATETIME updated_at
    }

    REVIEWS {
        CHAR(36) id PK
        TEXT     text
        INT      rating "1–5"
        CHAR(36) user_id  FK
        CHAR(36) place_id FK
        DATETIME created_at
        DATETIME updated_at
        UNIQUE   (user_id, place_id)
    }

    AMENITIES {
        CHAR(36) id PK
        VARCHAR  name "UNIQUE"
        DATETIME created_at
        DATETIME updated_at
    }

    PLACE_AMENITY {
        CHAR(36) place_id  FK
        CHAR(36) amenity_id FK
        PK       (place_id, amenity_id)
    }

    USERS   ||--o{ PLACES        : owns
    USERS   ||--o{ REVIEWS       : writes
    PLACES  ||--o{ REVIEWS       : receives
    PLACES  ||--o{ PLACE_AMENITY : contains
    AMENITIES ||--o{ PLACE_AMENITY : listed_in
