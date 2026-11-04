from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional , Annotated

class Patient(BaseModel):

    name : str
    email: EmailStr
    linkedin_url: AnyUrl
    age : int 
    weight: float
    married: bool
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, self):
        if self.age > 60 and 'emergency' not in self.contact_details:
            raise ValueError("patients older than 60 must have an emergency contact")
        return self

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)

patient_info = {
    'name': 'Lily',
    'email': 'lily@icic.com',
    'linkedin_url': 'https://linkedin.com/in/lily',
    'age': 70,
    'weight': 60.5,
    'married': False,
    'allergies': ['pollen'],
    'contact_details': {'phone': '1234567890','emergency':'783255'}
}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)

