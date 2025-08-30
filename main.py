from fastapi import FastAPI
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