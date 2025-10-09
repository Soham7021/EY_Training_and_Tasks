from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so frontend can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample student data
Stud = [
    {'id': 1, 'name': 'Soham', 'department': 'AI', 'Marks': 91},
    {'id': 2, 'name': 'Aniket', 'department': 'ENTC', 'Marks': 76},
    {'id': 3, 'name': 'Shreya', 'department': 'Civil', 'Marks': 36},
    {'id': 4, 'name': 'Rohit', 'department': 'AI', 'Marks': 79},
    {'id': 5, 'name': 'Ayush', 'department': 'IT', 'Marks': 86},
]

@app.get("/students")
def get_all_students():
    return {"Students": Stud}