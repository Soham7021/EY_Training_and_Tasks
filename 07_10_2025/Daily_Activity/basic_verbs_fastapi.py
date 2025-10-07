from fastapi import FastAPI

app = FastAPI()


@app.get("/students")
def get_students():
    return {"this is a get request"}


@app.post("/students")
def get_students():
    return {"this is a POST request"}


@app.put("/students")
def get_students():
    return {"this is a PUT request"}


@app.delete("/students")
def get_students():
    return {"this is a DELETE request"}