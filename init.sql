-- init.sql - Database initialization script

-- Check if the database exists, and create it if it doesn't
SELECT 'CREATE DATABASE tourism_chatbot'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'tourism_chatbot')
\gexec

\c tourism_chatbot;

-- Create tables (this will be handled by SQLAlchemy, but good to have as backup)
-- The tables will be created by your seed_data.py script

-- Remove the messagetype enum if it exists
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'messagetype') THEN
        DROP TYPE messagetype;
    END IF;
END $$;

-- Ensure the ephemeral_user exists with the correct password
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ephemeral_user') THEN
        CREATE ROLE ephemeral_user WITH LOGIN PASSWORD 'ephemeral_pass';
    END IF;
END $$;

-- Grant privileges to ephemeral_user
GRANT ALL PRIVILEGES ON DATABASE tourism_chatbot TO ephemeral_user;