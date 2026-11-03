from pydantic import BaseModel, EmailStr, AnyUrl
from typing import List, Dict, Optional

class Patient(BaseModel):

    name : str
    email: EmailStr
    linkedin_url: AnyUrl
    age : int
    weight: float
    married: bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.linkedin_url)
    print("inserted")

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("updated")

patient_info ={
    'name' : 'amna',
    'age' : 23,
    'email': 'octa@gmail.com',
    'linkedin_url': 'http://linkedin.com/in/123',
    'weight': 67.8,
    'married': True,
    'allergies':['pollen','dust'],
    'contact_details': {'phone': '787878'}
}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)
