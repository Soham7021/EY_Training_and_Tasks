from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {'message': 'Hello World'}

@app.get("/student/{student_id}")
def read_student(student_id: int):
    return {'student_id': student_id,'name':'Rahul','course':'AI'}