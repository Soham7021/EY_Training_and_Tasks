class Student:
    def __init__(self,name,age,email):
        self.name=name
        self.age=age
        self.email=email

data = {'name':'Aisha','age':20,'email':'aisha_123@gmail.com'}
student = Student(**data)
print(student.name)