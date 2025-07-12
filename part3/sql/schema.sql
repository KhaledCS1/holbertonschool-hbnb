\-- schema.sql – HBnB database schema
\-- Suhail Al‑aboud [10675@holbertonstudents.com](mailto:10675@holbertonstudents.com)

PRAGMA foreign\_keys = ON;

\-- ─────────────────────────────────────────────────────────────
\-- TABLE: users
\-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
id          CHAR(36) PRIMARY KEY,
first\_name  VARCHAR(255) NOT NULL,
last\_name   VARCHAR(255) NOT NULL,
email       VARCHAR(255) NOT NULL UNIQUE,
password    VARCHAR(255) NOT NULL,
is\_admin    BOOLEAN      NOT NULL DEFAULT FALSE,
created\_at  DATETIME     DEFAULT CURRENT\_TIMESTAMP,
updated\_at  DATETIME     DEFAULT CURRENT\_TIMESTAMP
);

\-- ─────────────────────────────────────────────────────────────
\-- TABLE: amenities
\-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS amenities (
id         CHAR(36) PRIMARY KEY,
name       VARCHAR(255) NOT NULL UNIQUE,
created\_at DATETIME     DEFAULT CURRENT\_TIMESTAMP,
updated\_at DATETIME     DEFAULT CURRENT\_TIMESTAMP
);

\-- ─────────────────────────────────────────────────────────────
\-- TABLE: places
\-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS places (
id          CHAR(36) PRIMARY KEY,
title       VARCHAR(255) NOT NULL,
description TEXT,
price       DECIMAL(10, 2) NOT NULL,
latitude    FLOAT,
longitude   FLOAT,
owner\_id    CHAR(36)     NOT NULL,
created\_at  DATETIME     DEFAULT CURRENT\_TIMESTAMP,
updated\_at  DATETIME     DEFAULT CURRENT\_TIMESTAMP,
FOREIGN KEY (owner\_id) REFERENCES users(id)
);

\-- ─────────────────────────────────────────────────────────────
\-- TABLE: reviews
\-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reviews (
id         CHAR(36) PRIMARY KEY,
text       TEXT        NOT NULL,
rating     INT         NOT NULL CHECK (rating BETWEEN 1 AND 5),
user\_id    CHAR(36)    NOT NULL,
place\_id   CHAR(36)    NOT NULL,
created\_at DATETIME     DEFAULT CURRENT\_TIMESTAMP,
updated\_at DATETIME     DEFAULT CURRENT\_TIMESTAMP,
UNIQUE (user\_id, place\_id),
FOREIGN KEY (user\_id)  REFERENCES users(id),
FOREIGN KEY (place\_id) REFERENCES places(id)
);

\-- ─────────────────────────────────────────────────────────────
\-- TABLE: place\_amenity  (association table Many‑to‑Many)
\-- ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS place\_amenity (
place\_id   CHAR(36) NOT NULL,
amenity\_id CHAR(36) NOT NULL,
PRIMARY KEY (place\_id, amenity\_id),
FOREIGN KEY (place\_id)   REFERENCES places(id),
FOREIGN KEY (amenity\_id) REFERENCES amenities(id)
);
