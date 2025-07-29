from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Dict, List, Optional

class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: str
    age: int
    weight: float
    married: bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['tcs.com', 'hcl.com']
        domain = value.split('@')[-1]

        if domain not in valid_domains:
            raise ValueError("We don't have tie up with the given company.")

        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

    @field_validator('age', mode='after')
    @classmethod
    def age_validator(cls, value):
        if 0 < value < 120:
            return value
        else:
            raise ValueError("Age is Invalid!")

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.email)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@tcs.com', 'linkedin_url':'http://linkedin.com/1322',
                'age': '30', 'married': True, 'weight': 75.2,'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)

