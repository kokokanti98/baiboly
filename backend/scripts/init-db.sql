-- Database initialization script for PostgreSQL
-- This script runs automatically when the PostgreSQL container is first created

-- Ensure UTF-8 encoding
SET client_encoding = 'UTF8';

-- Grant all privileges to baiboly_user on the baiboly_dev database
GRANT ALL PRIVILEGES ON DATABASE baiboly_dev TO baiboly_user;

-- Connect to the database
\c baiboly_dev

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO baiboly_user;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- For fuzzy text search

-- Grant default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO baiboly_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO baiboly_user;

-- Create a function to update tsvector on insert/update
CREATE OR REPLACE FUNCTION update_verset_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.texte_search_vector := to_tsvector('simple', COALESCE(NEW.texte, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Note: The trigger will be created after the verset table is created by migrations
-- This is just a preparation script
