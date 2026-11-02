
from fastapi import FastAPI , Path
from fastapi import HTTPException
import json

app = FastAPI(
    title="FastAPI for AI",
    description="A beginner-friendly API for learning backend development",
    version="1.0.0"
)

def load_data():
    with open('file.json','r') as f:
        data = json.load(f)
    return data

@app.get("/items/")
async def read_items(q: str | None = None):
    items = [
        {"course": "FastAPI"},
        {"level": "Beginner"},
        {"duration": "One week"}
    ]

    if q:
        return {"items": items, "q": q}

    return {"items": items}


@app.get("/about")
def about():
    return {
        "Hospital": "abcde hospital",
        "address": "xyza",
        "status": "open 24h"
    }


@app.get("/departments")
def skills():
    return {
        "departments": [
            "CARDIOLOGY",
            "NEUROLOGY",
            "PEDIATRICS",
            "DERMATOLOGY"
        ]
    }

@app.get("/patient/{patient_id}")
def get_patient(patient_id: int = Path(..., description="ID of the patient in the db", example='1002')):
    data = load_data()

    for patient in data["patients"]:
        if patient["patient_id"] == patient_id:
            return patient

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )




@app.get("/search")
def search_patient(name: str = "Ali"):
    return {
        "search_name": name,
        "message": "Search completed"
    }

@app.get("/view")
def view():
    data = load_data()
    return data



@app.get("/patients")
def get_patients(
    sort: str = "patient_id",
    order: str = "asc"
):
    data = load_data()
    patients = data["patients"]

    if sort not in ["age", "name", "patient_id"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be asc or desc")

    return sorted(
        patients,
        key=lambda patient: patient[sort],
        reverse=(order == "desc")
    )

