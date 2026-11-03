from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
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

## When a hospital gives some unique emails discount for medical , how do you seperate those emails...
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdf.com','icic.com']

        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('not a valid domain')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls,value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('age should be in beween 0 and 100')

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)

patient_info = {
    'name': 'Lily',
    'email': 'lily@icic.com',
    'linkedin_url': 'https://linkedin.com/in/lily',
    'age': 30,
    'weight': 60.5,
    'married': False,
    'allergies': ['pollen'],
    'contact_details': {'phone': '1234567890'},
}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)

