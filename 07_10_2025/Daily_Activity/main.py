from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    age: int
    course: str

students = [
    {'id':1, 'name':'Rahul', 'age':21, 'course':'AI'},
    {'id':2, 'name':'Priya', 'age':21, 'course':'AI'},
]
@app.get("/students")
def get_all_students():
    return {'students': students}

@app.get("/students/{student_id}")
def read_student(student_id: int):
    for s in students:
        if s['id'] == student_id:
            return s
    raise HTTPException(status_code=404, detail="student not found")


@app.post("/students",status_code=201)
def create_student(student: Student):
    students.append(student.dict())
    return {'message':'student created','student':student}

@app.put("/students/{student_id}")
def update_student(student_id: int, updated_student: Student):
    for i,s in enumerate(students):
        if s['id'] == student_id:
            students[i] = updated_student.dict()
            return {'message':'student updated','student':updated_student}

    raise HTTPException(status_code=404, detail="student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i,s in enumerate(students):
        if s['id'] == student_id:
            students.pop(i)
            return {'message':'student deleted','student':s}

    raise HTTPException(status_code=404, detail="student not found")