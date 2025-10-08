from http.client import responses

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_employee():
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_employee():
    empl = {
        "id": 5,
        "name": "Sam",
        "department": "Male",
        "salary":390094.2

    }
    response = client.post("/employees", json=empl)
    assert response.status_code == 200
    assert response.json()['salary'] == 390094.2

def test_get_employee_with_emp_id():
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json()["name"]=="Soham"

def test_emp_not_found():
    response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "employee not found"

def test_emp_update():
    empl = {
        "id": 1,
        "name": "Soham N",
        "department": "Consulting",
        "salary": 20000
    }

    response = client.put("/employees/1", json=empl)
    assert response.status_code == 200
    assert response.json()[0]['name'] == empl['name']

def test_emp_delete():
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json()['message'] == 'book deleted'