# run API with command : uvicorn <.py filename>:<FastAPI instance> --reload; e.g. uvicorn working:app --reload
# <URL>/docs to open API documentation page
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

class Inventory(BaseModel):
    data: Dict[int, Item]

inventory = {
    1: {
        "name" : "Milk",
        "price" : 12.99,
        "brand" : "Dutch Lady"
    },
    2: {
        "name" : "Cracker",
        "price" : 7.99,
        "brand" : "Julie"
    },
    3: {
        "name" : "Bread",
        "price" : 3.99,
        "brand" : "Massimo"
    },
    4: {
        "name" : "Milk",
        "price" : 11.99,
        "brand" : "Farm Fresh"
    },
}

app = FastAPI()

# http://127.0.0.1:8000/
@app.get('/')
def home():
    return {'health_check' : 'active'}

# http://127.0.0.1:8000/get-item/2
# http://127.0.0.1:8000/get-item/0; return error due to out-of-bound `item_id`
@app.get('/get-item/{item_id}')
def get_item(item_id: int = Path(1, description="Item ID to be viewed from `inventory`", ge=1, le=25)):
    return inventory[item_id]

# http://127.0.0.1:8000/get-item/4/price
@app.get('/get-item/{item_id}/{key}')
def get_item(item_id: int, key: str):
    return inventory[item_id][key]

# http://127.0.0.1:8000/get-by-name?name=Milk
# http://127.0.0.1:8000/get-by-name?name=Milk&brand=Farm%20Fresh
@app.get('/get-by-name')
def get_item(name: str, brand: Optional[str] = None):
    for item_id in inventory:
        if brand == None and \
            inventory[item_id]["name"] == name:
            return inventory[item_id]

        if inventory[item_id]["name"] == name and \
            inventory[item_id]["brand"] == brand:
            return inventory[item_id]
            
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name and/or brand not found")

# when var (item) inherits a class (Item), value(s) is expected to be passed in req body
# create entry
@app.post("/add-item/{item_id}")
def add_item(item: Item, item_id: int):
    if item_id in inventory:
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item ID already exists")

    inventory[item_id] = item
    return inventory[item_id]

# update entry
@app.put("/add-item/{item_id}")
def add_item(item: UpdateItem, item_id: int):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")

    if item.name != None:
        inventory[item_id]['name'] = item.name
    if item.price != None:
        inventory[item_id]['price'] = item.price
    if item.brand != None:
        inventory[item_id]['brand'] = item.brand
    return inventory[item_id]

@app.delete("/delete-item/{item_id}")
def delete_item(item_id: int = Query(..., description="Item ID to be deleted from `inventory`")):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")
    del inventory[item_id]
    return {"Success": f"Item ID: {item_id} is deleted"}