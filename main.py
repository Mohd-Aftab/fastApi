from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

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