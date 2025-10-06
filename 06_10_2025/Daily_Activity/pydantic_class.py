from pydantic import BaseModel

class Student(BaseModel):

    name : str
    age : int
    email : str
    is_active : bool = True


data = {'name':'Aisha','age':"20",'email':'aisha_123@gmail.com','is_active':False}
student = Student(**data)
print(student.age)