from pydantic import BaseModel, Field, EmailStr, model_validator
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

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.email)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@tcs.com', 'linkedin_url':'http://linkedin.com/1322',
                'age': '70', 'married': True, 'weight': 75.2,
                'contact_details':{'phone':'2353462', 'emergency': '9137091370'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)

