from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uvicorn
import urllib
from sqlalchemy.engine import URL
from enum import Enum
import sqlalchemy
from typing import List

#Connect to the database
db_server = "DESKTOP-25RH9IF\SQLEXPRESS"
db_name = "Animals"
db_driver = "ODBC Driver 17 for SQL Server"

params = urllib.parse.quote_plus(f"DRIVER={db_driver};SERVER={db_server};DATABASE={db_name};Trusted_Connection=yes")
db = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
Session = sessionmaker(bind=db)
Base = declarative_base()

db_url = URL.create("mssql+pyodbc", query={"odbc_connect": params})

#Define Database Models
class Conservation_status(Enum):
    Least_Concern = 1
    Near_Threatened = 2
    Endangered = 3
    Critically_Endangered = 4
    Extinct = 5

class Animal(Base):
    __tablename__ = "animal_data"
    animal_id = Column(Integer, primary_key=True, index=True)
    common_name = Column(String)
    scientific_name = Column(String)
    population = Column(Integer)
    conservation_status = Column(sqlalchemy.Enum(Conservation_status))
    native_region = Column(String)

# Define the API request/response models
class AnimalIn(BaseModel):
    common_name: str
    scientific_name: str
    population: int
    conservation_status: str
    native_region: str


class AnimalOut(AnimalIn):
    id: int


#Setting up the API
app = FastAPI()


# Define API endpoints

#Get ALL animals
@app.get("/animals", response_model=List[AnimalOut])
def read_animals():
    db = Session()
    animals = db.query(Animal).all()
    return animals

#Get one animal by providing the ID
@app.get("/animals/{animal_id}", response_model=AnimalOut)
def read_animal(animal_id: int):
    db = Session()
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

# Endpoint to get all conservation statuses
@app.get("/conservation-status")
async def get_all_conservation_statuses():
    return {"statuses": [status.value for status in Conservation_status]}

# Endpoint to add a new conservation status
@app.post("/conservation-status")
async def add_conservation_status(status: Conservation_status):
    # Logic to add new status to your database

    # Return the newly added status with its corresponding ID
    return {"id": 1, "status": status.value}

#Create animal
@app.post("/animals", response_model=AnimalOut)
def create_animal(animal: AnimalIn):
    db = Session()
    new_animal = Animal(**animal.dict())
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return new_animal

#Update animal
@app.put("/animals/{animal_id}", response_model=AnimalOut)
def update_animal(animal_id: int, animal: AnimalIn):
    db = Session()
    animal_db = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal_db:
        raise HTTPException(status_code=404, detail="Animal not found")
    for field, value in animal.dict(exclude_unset=True).items():
        setattr(animal_db, field, value)
    db.add(animal_db)
    db.commit()
    db.refresh(animal_db)
    return animal_db

# Search animal by name
@app.get("/animals/search/{name}", response_model=List[AnimalOut])
def search_animals(name: str):
    db = Session()
    animals = db.query(Animal).filter(or_(Animal.common_name.like(f"%{name}%"), Animal.scientific_name.like(f"%{name}%"))).all()
    if not animals:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animals

#Delete animal
@app.delete("/animals/{animal_id}")
def delete_animal(animal_id: int):
    db = Session()
    animal = db.query(Animal).filter(Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    db.delete(animal)
    db.commit()
    return {"message": "Animal deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)