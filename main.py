from fastapi import FastAPI , Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI(
    title="FastAPI for AI",
    description="A beginner-friendly API for learning backend development",
    version="1.0.0"
)
## using this pydantic model to post data in FastAPI ...
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
            return 'overweight'
        else:
            return ' obese'

## creating a pydantic model to put request in FastAPI ...
class PatientUpdate(BaseModel):

    id: Annotated[Optional[str], Field(default=None)]
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(gt=0, default=None)]
    gender: Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height: Annotated[Optional[float], Field(default=None,gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
  
## it helps us to access data by calling the fn
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
def get_patient(patient_id: str = Path(..., description="ID of the patient in the db", examples=['P001'])):
    data = load_data()
    patient_id = patient_id.upper()

    if patient_id in data:
        return {"id": patient_id, **data[patient_id]}

    raise HTTPException(status_code=404, detail="Patient not found")


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
def get_patients(sort: str = "id", order: str = "asc"):
    data = load_data()
    patients = [{"id": pid, **info} for pid, info in data.items()]

    if sort not in ["id", "name", "city", "age", "height", "weight", "bmi"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Order must be asc or desc")

    return sorted(
        patients,
        key=lambda patient: patient[sort],
        reverse=(order == "desc")
    )
## adding new data to the database ...
@app.post('/create')
def create_patient(patient:Patients):
    ## load existing data
    data = load_data()

    ## check if the patient alreday exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient alreday exists')
    
    ## add new patient to the database
    data[patient.id] = patient.model_dump(exclude={'id'})

    ## save into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'mesage': 'patient created successfully...'})

## Put request in FastAPI endpoint ...
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found in the database.')

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    ## making pydantic object from Patients class so that when we update weight, it also calculates bmi & verdict based on weight ...
    ## existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patients(**existing_patient_info)

    ## -> pydantic object -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    ## add this dict to data
    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})

## To delete a patient info
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient does not exist in the database. ')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message ' : 'Patient deleted. '})
