from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

class Book(BaseModel):
    id:int
    title:str
    author:str
    price:float
    in_stock:bool

buk = [
    {'id':1,'title':'Harry','author':'Soham','price':200,'in_stock':True},
    {'id':2,'title':'Dune','author':'Rohit','price':408.2,'in_stock':False},
    {'id':3,'title':'History','author':'Soham','price':500,'in_stock':True},
]

app = FastAPI()
@app.get("/books")
def get_books():
    return {'Books':buk}

@app.get("/books/Available")
def get_books_available():
    available_books = [book for book in buk if book['in_stock']]
    if available_books:
        return available_books
    raise HTTPException(status_code=404, detail="No books available")

@app.get("/books/count")
def get_books_count():
    a = 0
    for i in buk:
        if i['in_stock']:
            a += 1
    return {'Total count of Books Available':a}

@app.get("/books/search")
def get_author_price(author: str = None, max_price: float = None):
    a = []
    for i in buk:
        if author and max_price is not None:
            if i['author'].lower() == author.lower() and i['price'] <= max_price:
                a.append(i)
        elif author:
            if i['author'].lower() == author.lower():
                a.append(i)
        elif max_price is not None:
            if i['price'] <= max_price:
                a.append(i)
    if not a:
        raise HTTPException(status_code=404, detail="No books available")
    return a





@app.get("/books/{book_id}")
def get_book(book_id: int):
    for i in buk:
        if i['id'] == book_id:
            return i

    raise HTTPException(status_code=404, detail="book not found")



@app.post("/books")
def create_book(book: Book):
    for i in buk:
        if i['id'] == book.id:
            raise HTTPException(status_code=404, detail="book already exists with the same name")

        if book.price < 0:
            raise HTTPException(status_code=404, detail="book price cannot be negative")

    buk.append(book.dict())
    return {'message':'book created','book':book}

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    for i,s in enumerate(buk):
        if s['id'] == book_id:
            buk[i] = book.dict()
            return {'message':'book updated','book':book}
    raise HTTPException(status_code=404, detail="book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i in buk:
        if i['id'] == book_id:
            buk.remove(i)
            return {'message':'book deleted','book':buk}

    raise HTTPException(status_code=404, detail="book not found")