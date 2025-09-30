# CamTour Backend

## Database Setup
1. Ensure you have Docker and Docker Compose installed on your machine.
2. Clone the repository and navigate to the project directory.
3. Create a `.env` file in the root directory and configure your database connection settings.
4. Run the following command to start the PostgreSQL and Adminer containers:
   ```
   docker-compose up -d
   ```
5. Access Adminer at `http://localhost:8080` and log in with the following credentials:
  - Adminer: http://localhost:8080
  - System: PostgreSQL
  - Server: postgres
  - Username: postgres
  - Password: password
  - Database: chatbot_db