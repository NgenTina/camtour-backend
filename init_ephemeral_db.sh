#!/bin/bash

# Wait for the ephemeral database to be ready
until PGPASSWORD=ephemeral_pass psql -h localhost -p 5433 -U ephemeral_user -d ephemeral_db -c "\q"; do
  echo "Waiting for ephemeral database to be ready..."
  sleep 2
done

# Apply schema
PGPASSWORD=ephemeral_pass psql -h localhost -p 5433 -U ephemeral_user -d ephemeral_db -f init.sql

# Seed data
python seed_data.py