from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional , Annotated

class Patient(BaseModel):

    name : Annotated[str , Field(max_length=50, title='The name of the patient', description='write the name in less than 30 characcters ', examples=['amna','anisha','amit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age : int = Field(gt=0, lt=110)
    weight: float = Field(gt=0)
    married: bool
    allergies: Optional[List[str]] = Field(max_length=50)
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
