# FastAPI Boilerplate

This is a boilerplate project for creating production-ready FastAPI applications. It includes a structured layout, database integration with Alembic for migrations, JWT authentication, and more.

## Features

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: The Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- **Alembic**: A lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **JWT Authentication**: Secure your endpoints with JSON Web Tokens.
- **Dependency Management**: Using `uv` for fast and reliable dependency management.
- **Docker Support**: Includes `Dockerfile` and `docker-compose.yml` for easy containerization.
- **Structured Logging**: Using `structlog` for clear and structured logs.
- **CORS**: Cross-Origin Resource Sharing (CORS) middleware.
- **Makefile**: Convenient commands for common tasks.

## Project Structure

```
.
├── app
│   ├── core
│   │   ├── config.py
│   │   └── logging.py
│   ├── db
│   │   ├── migration.py
│   │   ├── query_builder.py
│   │   ├── session.py
│   │   └── models
│   │       ├── __init__.py
│   │       ├── base.py
│   │       └── user.py
│   ├── middleware
│   │   └── logging_midleware.py
│   ├── redis
│   │   └── redis_instance.py
│   ├── routes
│   │   ├── api_router.py
│   │   ├── auth_routes.py
│   │   ├── health_routes.py
│   │   └── user_routes.py
│   ├── schemas
│   │   ├── auth.py
│   │   ├── response.py
│   │   └── user.py
│   ├── services
│   │   ├── auth_service.py
│   │   └── user_service.py
│   ├── shared
│   │   └── constants.py
│   └── utlis
│       ├── generateJwt.py
│       └── verifyPwd.py
├── logs
├── migrations
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
└── README.md
```

## Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```
# .env
APP_NAME="FastAPI-BoilerPlate"
APP_ENV="development"
DEBUG=True
STRUCTURED_LOGGING=True

# Server Settings
HOST="0.0.0.0"
PORT=8000
RELOAD=True

# Security
SECRET_KEY="your-secret-key"
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM="HS256"

# Database
DATABASE_URL="postgresql://user:password@localhost/mydatabase"
MIGRATION=True

# CORS
CORS_METHOD='["*"]'
CORS_ORIGIN='["*"]'
CORS_HEADER='["*"]'

# Logging
LOG_LEVEL="info"
LOG_FILE="logs/app.log"
SAVE_LOG=True

# Redis
REDIS_HOST="localhost"
REDIS_PORT=6379
REDIS_DB=0
```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/FastAPI-Boilerplate.git
    cd FastAPI-Boilerplate
    ```

2.  **Install dependencies using `uv`:**

    ```bash
    make install
    ```

## Running the Project

To run the development server, use the following command:

```bash
make run
```

The application will be available at `http://localhost:8000`.

## Running with Docker

1.  **Build the Docker image:**

    ```bash
    docker-compose build
    ```

2.  **Run the services:**

    ```bash
    docker-compose up
    ```

The application will be available at `http://localhost:8000`.

## API Endpoints

### Health

-   `GET /health`: Check the health of the application.

### Authentication

-   `POST /auth/signup`: Create a new user.
-   `POST /auth/login`: Log in and get a JWT token.

### Users

-   `GET /user`: Get a list of users.
-   `GET /user/{user_id}`: Get a user by ID.
-   `POST /user`: Create a new user.
-   `PATCH /user/{user_id}`: Update a user.
-   `DELETE /user/{user_id}`: Delete a user.

## Project Commands

The `Makefile` includes several commands to streamline development:

-   `make install`: Install project dependencies.
-   `make run`: Run the development server.
-   `make lint`: Lint the code using Ruff.
-   `make format`: Format the code using Ruff.
-   `make test`: Run tests.
-   `make db-migration msg="your message"`: Create a new database migration.
-   `make db-upgrade`: Apply database migrations.
-   `make db-downgrade`: Downgrade the database by one migration.
-   `make clean`: Clean up temporary files.