# Spy Cat Agency (SCA) Management System

A RESTful API application for managing spy cats, missions, and targets.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Validation**: Pydantic
- **External API**: TheCatAPI for breed validation

## Setup & Installation

### Prerequisites
- Python 3.9+

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SpyCatAgency
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8080`

### API Documentation

Once running, you can access:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## API Endpoints

### Spy Cats

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cats/` | Create a new spy cat |
| GET | `/cats/` | List all spy cats |
| GET | `/cats/{cat_id}` | Get a single spy cat |
| PATCH | `/cats/{cat_id}` | Update spy cat's salary |
| DELETE | `/cats/{cat_id}` | Remove a spy cat |

### Missions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/missions/` | Create a new mission with targets |
| GET | `/missions/` | List all missions |
| GET | `/missions/{mission_id}` | Get a single mission |
| DELETE | `/missions/{mission_id}` | Delete a mission (if not assigned) |
| PATCH | `/missions/{mission_id}/assign` | Assign a cat to a mission |

### Targets

| Method | Endpoint | Description |
|--------|----------|-------------|
| PATCH | `/targets/{target_id}` | Update target notes or mark complete |

## Request/Response Examples

### Create a Spy Cat
```json
POST /cats/
{
    "name": "Whiskers",
    "years_of_experience": 5,
    "breed": "Persian",
    "salary": 50000.00
}
```

### Create a Mission with Targets
```json
POST /missions/
{
    "cat_id": null,
    "targets": [
        {
            "name": "Target Alpha",
            "country": "Germany",
            "notes": "Initial reconnaissance"
        },
        {
            "name": "Target Beta",
            "country": "France",
            "notes": ""
        }
    ]
}
```

### Assign Cat to Mission
```json
PATCH /missions/1/assign
{
    "cat_id": 1
}
```

### Update Target
```json
PATCH /targets/1
{
    "notes": "Updated intelligence gathered",
    "complete": true
}
```

## Business Rules

1. **Spy Cats**:
   - Breed must be validated against TheCatAPI
   - Only salary can be updated after creation

2. **Missions**:
   - Must have between 1 and 3 targets
   - Cannot be deleted if assigned to a cat
   - Automatically marked complete when all targets are complete

3. **Targets**:
   - Notes cannot be updated if target or mission is complete
   - Once marked complete, cannot be reverted

4. **Assignments**:
   - A cat can only have one active mission at a time
   - Cannot assign a cat to a completed mission

## Postman Collection

Import the following collection to test the API:

[Postman Collection Link](https://www.postman.com/collections/spy-cat-agency)

Or use the file: `postman_collection.json` in this repository.

## Project Structure

```
SpyCatAgency/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── app/
│   ├── __init__.py
│   ├── database.py        # Database configuration
│   ├── models/            # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── spy_cat.py
│   │   ├── mission.py
│   │   └── target.py
│   ├── schemas/           # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── spy_cat.py
│   │   ├── mission.py
│   │   └── target.py
│   ├── routers/           # API endpoints
│   │   ├── __init__.py
│   │   ├── cats.py
│   │   ├── missions.py
│   │   └── targets.py
│   └── services/          # External services
│       ├── __init__.py
│       └── cat_api.py     # TheCatAPI integration
└── postman_collection.json # Postman collection
```

## License

MIT

