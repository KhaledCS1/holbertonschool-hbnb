erDiagram

    users {
        CHAR(36)  id           PK
        VARCHAR   first_name
        VARCHAR   last_name
        VARCHAR   email        "UNIQUE"
        VARCHAR   password
        BOOLEAN   is_admin
        DATETIME  created_at
        DATETIME  updated_at
    }

    places {
        CHAR(36)  id           PK
        VARCHAR   title
        TEXT      description
        DECIMAL   price
        FLOAT     latitude
        FLOAT     longitude
        CHAR(36)  owner_id     FK
        DATETIME  created_at
        DATETIME  updated_at
    }

    reviews {
        CHAR(36)  id           PK
        TEXT      text
        INT       rating       "1–5"
        CHAR(36)  user_id      FK
        CHAR(36)  place_id     FK
        DATETIME  created_at
        DATETIME  updated_at
        UNIQUE    (user_id, place_id)
    }

    amenities {
        CHAR(36)  id           PK
        VARCHAR   name         "UNIQUE"
        DATETIME  created_at
        DATETIME  updated_at
    }

    place_amenity {
        CHAR(36)  place_id     FK
        CHAR(36)  amenity_id   FK
        PK        (place_id, amenity_id)
    }

    users      ||--o{ places        : owns
    users      ||--o{ reviews       : writes
    places     ||--o{ reviews       : receives
    places     ||--o{ place_amenity : contains
    amenities  ||--o{ place_amenity : listed_in
