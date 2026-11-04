from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional , Annotated

class Patient(BaseModel):

    name : str
    email: EmailStr
    linkedin_url: AnyUrl
    age : int 
    weight: float
    height: float
    married: bool
    allergies: Optional[List[str]]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    
def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print('BMI',patient.calculate_bmi)

patient_info = {
    'name': 'Lily',
    'email': 'lily@icic.com',
    'linkedin_url': 'https://linkedin.com/in/lily',
    'age': 70,
    'weight': 60.5,
    'height': 1.72,
    'married': False,
    'allergies': ['pollen'],
    'contact_details': {'phone': '1234567890','emergency':'783255'}
}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)

