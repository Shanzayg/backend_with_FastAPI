from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address


address_dict = {'city': 'Faisalabad', 'state': 'Punjab', 'pin': '38000'}
address1 = Address(**address_dict)

patient_dict = {
    'name': 'Lily',
    'gender': 'female',
    'age': 35,
    'address': address1,   # a plain dict like address_dict also works
}
patient1 = Patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.pin)

temp = patient1.model_dump()
temp = patient1.model_dump_json()

print(temp)
print(type(temp))