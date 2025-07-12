\-- data.sql – initial data for HBnB database
\-- Suhail Al‑aboud [10675@holbertonstudents.com](mailto:10675@holbertonstudents.com)

\-- ─────────────────────────────────────────────────────────────
\-- Admin user (password = "admin1234" bcrypt‑hashed)
\-- ─────────────────────────────────────────────────────────────
INSERT INTO users (id, first\_name, last\_name, email, password, is\_admin)
VALUES (
'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
'Admin',
'HBnB',
'[admin@hbnb.io](mailto:admin@hbnb.io)',
'\$2b\$12\$M70NZLi7MQqj1yenGT.rzOjW8lcrsHQhSNDnGyWKljrnOHJ4NA4p6',
TRUE
);

\-- ─────────────────────────────────────────────────────────────
\-- Initial amenities
\-- ─────────────────────────────────────────────────────────────
INSERT INTO amenities (id, name) VALUES
('15522fd4-c875-4f03-8a05-2785e19af580', 'WiFi'),
('d85b85d9-6cad-4250-805b-a3a4476b3a3d', 'Swimming Pool'),
('9300d3f0-fc97-447f-bb9f-d41528856a15', 'Air Conditioning');
