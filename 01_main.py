from fastapi import FastAPI , Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI(
    title="FastAPI for AI",
    description="A beginner-friendly API for learning backend development",
    version="1.0.0"
)

class Patients(BaseModel):

    id: Annotated[str, Field(..., description='id of the pateint')]
    name: Annotated[str, Field(..., description='name of the pateint')]
    city: Annotated[str, Field(..., description='city where the pateint is living')]
    age: Annotated[int, Field(..., lt=110, gt=0, description='Age of the patient')]
    gender: Annotated[Literal['male','female','others'],Field(..., description='gender of the patient')]
    height: Annotated[float, Field(..., description='height of the patient in mtrs')]
    weight: Annotated[float, Field(..., description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'normal'
        else:
            return ' obese'
  

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

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


## Path Parameters
@app.get("/patient/{patient_id}")
def get_patient(patient_id: int = Path(..., description="ID of the patient in the db", examples='1002')):
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


## HTTP status codes
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

@app.post('/create')
def create_patient(patient:Patients):
    ## load existing data
    data = load_data()

    ## check if the patient alreday exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient alreday exists')
    
    ## add new patient to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    ## save into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'mesage': 'patient created successfully...'})
