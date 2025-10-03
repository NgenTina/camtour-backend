uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

 uv pip install pydantic[email] --link-mode=copy

 Start the Database
Make sure your ephemeral Postgres database is running. You can use Docker Compose:

docker-compose up ephemeral_db

Seed the Database (Optional)
You can seed the database with sample data:

python seed_data.py

Or, use the /seed endpoint if running the FastAPI server.

Run the FastAPI Server
Start your backend server:

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

