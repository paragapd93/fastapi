from pydantic import BaseModel, Field, EmailStr, computed_field
from typing import Dict, List, Optional

class Patient(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: str
    age: int
    weight: float #in kg
    height: float #in meter
    married: bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.email)
    print(patient.calculate_bmi)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@tcs.com', 'linkedin_url':'http://linkedin.com/1322',
                'age': '70', 'married': True, 'weight': 72.2, "height": 1.73,
                'contact_details':{'phone':'2353462', 'emergency': '9137091370'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)

