# User Management API

A simple FastAPI application for managing users with MongoDB using Beanie ODM.

## Prerequisites

- Python 3.12
- MongoDB (or Docker for containerized setup)
- PDM package manager (for local development)

## Running with Docker (Recommended)

### Start the application and MongoDB:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

### Stop the application:
```bash
docker-compose down
```

### Stop and remove volumes (clean slate):
```bash
docker-compose down -v
```

## Local Development

### Installation

```bash
pdm install
```

### Running the API

```bash
uvicorn mongo_db_communication_libraries.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Create User
```http
POST /users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Get User by ID
```http
GET /users/{user_id}
```

### Delete User
```http
DELETE /users/{user_id}
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

- `MONGODB_URL` - MongoDB connection string (default: `mongodb://localhost:27017`)
- `DATABASE_NAME` - Database name (default: `users_db`)

## Beanie Migrations

**Important Note:** Beanie does not require traditional migrations like Django or Alembic because:

1. **Schema-less MongoDB**: MongoDB is schema-less, so collections are created automatically when documents are inserted.
2. **Automatic Index Creation**: Beanie automatically creates indexes defined in your Document models.
3. **Document Model Evolution**: You can modify your Document classes, and Beanie handles the changes gracefully.

### What Beanie Does Automatically:
- Creates collections when first document is inserted
- Creates indexes defined in `Settings.indexes`
- Validates documents against your Pydantic models

### If You Need Manual Schema Management:

For advanced scenarios (like data transformations or complex index changes), you can:

1. **Create a migration script:**
```python
# scripts/migrate.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from mongo_db_communication_libraries.entities.user_entity import User

async def migrate():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=client.users_db, document_models=[User])
    
    # Your migration logic here
    # Example: Add a new field to existing documents
    await User.find().update({"$set": {"new_field": "default_value"}})
    
    print("Migration completed!")

if __name__ == "__main__":
    asyncio.run(migrate())
```

2. **Run the migration:**
```bash
python scripts/migrate.py
```

### Best Practices:
- Beanie initializes your database schema automatically when the application starts
- Use `Settings.indexes` in your Document models to define indexes
- For production, consider using index management tools or scripts for complex index changes
- Document schema changes are handled through your Pydantic models - just update the model and restart
