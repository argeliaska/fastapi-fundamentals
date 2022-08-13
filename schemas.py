from pydantic import BaseModel
from typing import Optional, List
import json


class TripInput(BaseModel):
    start: int
    end: int
    description: str


class TripOutput(TripInput):
    id: int


class CarInput(BaseModel):
    size: str
    fuel: Optional[str] = 'electric'
    doors: int
    transmission: Optional[str] = 'auto'

    class Config:
        schema_extra = {
            "example" : {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }


class CarOutput(CarInput):
    id: int
    trips: List[TripOutput] = []

def load_db() -> List[CarOutput]:
    """Load a list of Car objects from a JSON file"""
    with open('cars.json') as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]

def save_db(cars: List[CarInput]):
    with open('cars.json', 'w') as f:
        json.dump([car.dict() for car in cars], f, indent=4)