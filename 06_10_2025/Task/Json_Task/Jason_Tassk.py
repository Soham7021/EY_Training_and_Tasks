import json
import logging


logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


student = [
    {"name": "Rahul", "age": 21, "course": "AI", "marks": 85},
    {"name": "Priya", "age": 22, "course": "ML", "marks": 90}
]


with open("student.json", 'w') as f:
    json.dump(student, f, indent=4)
    logging.info("Initial student data written to file")


try:
    with open("student.json", 'r') as f:
        data = json.load(f)
        logging.info("File read successfully")
        print("Student Names:")
        for student in data:
            print(student["name"])
        logging.info("Names printed")
except Exception as e:
    logging.error(f"File not read: {e}")
    data = []


new_student = {"name": "Arjun", "age": 20, "course": "Data Science", "marks": 78}
data.append(new_student)
logging.info("New student added")


with open("student.json", 'w') as f:
    json.dump(data, f, indent=4)
    logging.info("File saved successfully")