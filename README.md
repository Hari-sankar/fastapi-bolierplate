# FastAPI BoilerPlate Application

A robust production level backend application built using FastAPI.

## Features

- ⚡️ Fully async
- 🚀 Pydantic V2 and SQLAlchemy 2.0
- 🔐 User authentication with JWT
- 🍪 Cookie based refresh token
- 🏬 Easy redis caching
- 👜 Easy client-side caching
- 🛑 Rate Limiter dependency
- 🚚 Easy running with docker compose
- CORS, GZip, Static Files, Streaming responses.

## Prerequisites

- Python 3.12+
- UV
- FastAPI
- Pydantic
- Pyjwt
- Bcrypt
- Python-dotenv

## Setup & Installation

1. **Clone the Repository**

```
git clone https://github.com/doncjohn/fastapi_sample_app.git
```

2. **Install Dependencies**
``` 
pip install uv
```

4. **Environment Variables**

Copy the sample environment variables:
```
DATABASE_URL=postgresql://username:password@host/test
```

Update the `.env` file with your actual data.

5. **Initialize the Database**

```
db init
db migrate
db upgrade
```

6. **Run the Application**

Use the uv Dev Command

```
uv run dev
```

Use the uv Full command 
```
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

uv run fastapi dev
```

Navigate to [http://localhost:8000](http://localhost:8000)

## Testing

To run the tests:

```
pytest
```