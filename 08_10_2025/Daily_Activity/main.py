from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float

emp = [
    {'id':1,'name':'Soham','department':'Consulting','salary':20000},
    {'id':2,'name':'Aniket','department':'Accounts','salary':20038.2},
    {'id':3,'name':'Shreya','department':'Tax','salary':20000},
]

@app.get("/employees")
def get_all_employees():
    return {'employees': emp}

@app.post("/employees")
def post_employee(employee:Employee):
    emp.append(employee.dict())
    return employee

@app.get("/employees/{emp_id}")
def get_employee(emp_id:int):
    for i in emp:
        if i['id'] == emp_id:
            return i

    raise HTTPException(status_code=404, detail="employee not found")

@app.put("/employees/{emp_id}")
def put_employee(emp_id:int, employ:Employee):
    for i,s in enumerate(emp):
        if s['id'] == emp_id:
            emp[i] = employ.dict()
            return emp

    raise HTTPException(status_code=404, detail="employee not found")

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id:int):
    for i in emp:
        if i['id'] == emp_id:
            emp.remove(i)
            return {'message':'book deleted','book':i}

    raise HTTPException(status_code=404, detail="employee not found")