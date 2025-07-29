from fastapi import FastAPI, Path, Query, HTTPException
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=['Nitish'])]
    city: Annotated[str, Field(..., description="City of the patient", examples=['Siliguri'])]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0, lt=120, examples=[32])]
    gender: Annotated[Literal['male','female','others'], Field(..., description="gender of the Patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters", examples=['1.8'])]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in Kgs", examples=['60'])]

    #Computed field to calculate bmi
    @computed_field(return_type=float)
    @property
    def bmi(self):
        return round(self.weight/self.height**2, 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18:
            return "Underweight"
        elif self.bmi < 24:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data

#save the data back to the json/db
def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data, f)

@app.get("/")
def home():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "API to manage you patient records"}

@app.get("/view")
def view():
    data = load_data()

    return data

@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="ID of the Patient", example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        return {"error": f"patient with id: {patient_id} not found!"}

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"),
                  order: str = Query('asc', description="Sort in asc or desc order")):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field selected from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order selected other than asc or desc")

    data = load_data()
    sort_order = True if order=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):

    #load exisiting data
    data = load_data()

    #check whether the requested patient exists
    if patient.id in data.keys():
        raise HTTPException(status_code=400, detail="Patient already exists!")

    # If new patient then create the patient block
    else:
        data[patient.id] = patient.model_dump(exclude=['id'])
        save_data(data)

        return JSONResponse(status_code=201, content="Patient created Successfully!")



