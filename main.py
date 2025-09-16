from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):

    id : Annotated[str, Field(..., description="ID of the patient", example="P001")]
    name : Annotated[str, Field(..., description="Name of the patient", example="John Doe")]
    age : Annotated[int, Field(..., gt=0, le=120, description="Age of the patient", example=30)]
    gender : Annotated[Literal["male", "female", "other"], Field(..., description="Gender of the patient")]
    city : Annotated[str, Field(..., description="City of the patient", example="New York")]
    weight : Annotated[float, Field(..., gt=0, description="Weight of the patient in kg", example=70.5)]
    height : Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs", example=1.75)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Hello, World!"}
@app.get("/about")
def about():
    return {"message": "This is a simple about application."}

@app.get("/view")
def view_data():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def get_patient(patient_id : str = Path(..., description="ID of the patient", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str=Query(..., description="Sort patients by weight, height or bmi"),
                  order:  str=Query("asc", description="Order of sorting: asc or desc")):
    
    valid_fields = ["weight", "height", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(400, detail=f"Invalid fields , Please use the fields from {valid_fields}")
    
    order_by = True if order == "desc" else False

    data = load_data()

    sorted_data = sorted(data.values(),key=lambda x : x.get(sort_by, 0), reverse=order_by)

    return sorted_data

@app.post("/create")
def add_patient(patient:Patient):

    # Load data
    data = load_data()

    # check if existed
    if patient.id in data:
        raise HTTPException(400, detail=f"Patient Already existed")
    
    # add pateint to db
    data[patient.id] = patient.model_dump(exclude=["id"])

    # Return Json Object
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient added successfully"})
        