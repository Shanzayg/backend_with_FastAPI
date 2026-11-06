# Patient Management System API

A beginner-friendly REST API for managing patient records, built with **FastAPI** and **Pydantic**. It supports full CRUD (create, read, update, delete) and automatically calculates each patient's **BMI** and **health verdict** from their height and weight. Data is stored in a simple JSON file, so there is no database to set up.

## Features

- Create, view, update and delete patient records
- Automatic **BMI** and **verdict** (Underweight / Normal / Overweight / Obese) calculation using Pydantic computed fields
- Partial updates: send only the fields you want to change, and BMI and verdict are recalculated
- Sort patients by `id`, `name`, `city`, `age`, `height`, `weight` or `bmi`, ascending or descending
- Input validation (age range, gender options, positive height and weight)
- Interactive API docs with Swagger UI, generated automatically

## Tech Stack

- [Python](https://www.python.org/) 3.10+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- JSON file as the data store

## Project Structure

```
.
├── main.py          # FastAPI app: models and all endpoints
├── patients.json    # Patient data (acts as the database)
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

The API is now running at `http://127.0.0.1:8000`.

### 5. Open the interactive docs

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

### Patient endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/view` | Return the whole database |
| `GET` | `/patient/{patient_id}` | Get one patient by ID (e.g. `P001`) |
| `GET` | `/patients?sort=age&order=desc` | List all patients, sorted |
| `POST` | `/create` | Add a new patient |
| `PUT` | `/edit/{patient_id}` | Update one or more fields of a patient |
| `DELETE` | `/delete/{patient_id}` | Delete a patient |

**Query parameters for `/patients`**

| Parameter | Default | Options |
|-----------|---------|---------|
| `sort` | `id` | `id`, `name`, `city`, `age`, `height`, `weight`, `bmi` |
| `order` | `asc` | `asc`, `desc` |

### Demo endpoints

These were added while learning FastAPI basics (path and query parameters):

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/about` | Hospital information |
| `GET` | `/departments` | List of departments |
| `GET` | `/items/?q=...` | Query parameter example |
| `GET` | `/search?name=...` | Search example |

## Data Format

`patients.json` is a dictionary keyed by patient ID:

```json
{
  "P001": {
    "name": "Pooja Desai",
    "city": "Kolkata",
    "age": 31,
    "gender": "female",
    "height": 1.65,
    "weight": 44,
    "bmi": 16.16,
    "verdict": "Underweight"
  }
}
```

## Example Requests

### Create a patient

`POST /create`

```json
{
  "id": "P021",
  "name": "Asha Rao",
  "city": "Pune",
  "age": 29,
  "gender": "female",
  "height": 1.62,
  "weight": 58
}
```

`bmi` and `verdict` are calculated automatically, so don't send them.

Response: `201 Created`

```json
{ "message": "patient created successfully..." }
```

### Update a patient

`PUT /edit/P021`. Send only the fields you want to change:

```json
{ "weight": 70 }
```

BMI and verdict are recalculated from the new weight.

### Delete a patient

`DELETE /delete/P021`

### Using curl

```bash
# Get one patient
curl http://127.0.0.1:8000/patient/P001

# List patients sorted by age, oldest first
curl "http://127.0.0.1:8000/patients?sort=age&order=desc"

# Update a patient's weight
curl -X PUT http://127.0.0.1:8000/edit/P001 \
  -H "Content-Type: application/json" \
  -d '{"weight": 50}'
```

## BMI Verdicts

BMI = weight (kg) / height (m)²

| BMI | Verdict |
|-----|---------|
| below 18.5 | Underweight |
| 18.5 to 24.9 | Normal |
| 25 to 29.9 | Overweight |
| 30 and above | Obese |

## Validation Rules

| Field | Rule |
|-------|------|
| `id` | Required string, must be unique |
| `name`, `city` | Required strings |
| `age` | Integer greater than 0 and less than 110 |
| `gender` | One of `male`, `female`, `others` |
| `height` | Number in metres |
| `weight` | Number in kilograms |

## Error Responses

| Status | When |
|--------|------|
| `400` | Creating a patient whose ID already exists, or using an invalid `sort`/`order` value |
| `404` | Patient ID not found (get, edit or delete) |
| `422` | Request body fails validation (missing field, wrong type, out-of-range value) |

## Future Improvements

- Replace the JSON file with a real database such as SQLite or PostgreSQL
- Add authentication
- Add pagination and search by name or city
- Add automated tests with `pytest`

## License

This project is for learning purposes.