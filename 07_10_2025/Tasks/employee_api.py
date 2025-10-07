from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

app = FastAPI()

@app.get("/employee")
def read_employee():
    return {'employee':emp}

@app.get("/employee/count")
def read_employee_count():
    return {'count':len(emp)}


@app.get("/employee/{employee_id}")
def read_employee(employee_id: int):
    for i in emp:
        if i['id'] == employee_id:
            return i

    raise HTTPException(status_code=404, detail="employee not found")


@app.post("/employee")
def create_employee(employee: Employee):
    for i in emp:
        if i['id'] == employee.id:
            raise HTTPException(status_code=404, detail="employee already exists")
    emp.append(employee.dict())
    return {'message':'employee created','employee':emp}


@app.put("/employee/{employee_id}")
def update_employee(employee_id: int, up_employee: Employee):
    for i,s in enumerate(emp):
        if s['id'] == employee_id:
            emp[i] = up_employee.dict()
            return {'message':'employee updated','employee':up_employee.dict()}

    raise HTTPException(status_code=404, detail="employee not found")

@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int):
    for i in emp:
        if i['id'] == employee_id:
            emp.remove(i)
            return {'message':'employee deleted','employee':emp}

    raise HTTPException(status_code=404, detail="employee not found")