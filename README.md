### For the UV (Astral)

**Download Packages**
To install packages in the UV environment, use the following command:
```python
uv pip install <package-name> --link-mode=copy
```

---

### How to run the App

#### Testing Stage

**Start the Database**
Make sure your ephemeral Postgres database is running. You can use Docker Compose:

```bash
docker-compose up ephemeral_db
```

**Seed the Database (Optional)**
You can seed the database with sample data:

```bash
python seed_data.py
```

Or, use the `/seed` endpoint if running the FastAPI server.

**Run the FastAPI Server**
Start your backend server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Production Stage


---
### Tasks

- [x] Create a Dockerfile for the FastAPI application.
- [x] Defined chatbot models and endpoints.
- [ ] Implement core architecture and features of the application.
- [x] Create a persistent and ephemeral (temporary) database service in Docker Compose for production use.
- [ ] Ensure the FastAPI application connects to the persistent database in production.

### API Test Authentication

The authentication system in our project uses JWT (JSON Web Tokens) for securing API endpoints. Here's a high-level overview of how it works:


Build with Love by FAKER and NaQT