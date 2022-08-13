from fastapi import FastAPI, HTTPException
import uvicorn
from http import HTTPStatus
from typing import Dict, List, Optional

from schemas import load_db, save_db, CarInput, CarOutput, TripOutput, TripInput

app = FastAPI(title='FastAPI Car Sharing')

db = load_db()

@app.get('/api/cars')
# def get_cars(size:str|None=None, doors:int|None=None) -> list:
def get_cars(size:Optional[str]=None, doors:Optional[int]=None) -> List:
    """Return the list of cars"""
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors == doors]
    return result

@app.get('/api/cars/{id}')
def get_car_by_id(id:int) -> Dict:
    """Return the car that matches with the id"""
    result = [car for car in db if car.id == id]
    if result: 
        return result[0]
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'No car with id = {id}'
        )

@app.post('/api/cars', response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel,
                        transmission=car.transmission, id=len(db)+1)
    db.append(new_car)
    save_db(db)
    return new_car

@app.put('/api/cars/{id}', response_model=CarOutput)
def update_car(id:int, data: CarInput) -> CarOutput:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.size = data.size
        car.fuel = data.fuel
        car.doors = data.doors
        car.transmission = data.transmission
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail=f'No car with id={id}')        

@app.delete('/api/cars/{id}', status_code=HTTPStatus.NO_CONTENT)
def remove_car(id:int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail=f'No car with id={id}')

@app.post('/api/cars/{car_id}/trips', response_model=TripOutput)
def add_trip(car_id:int, trip:TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips)+1, 
                            start=trip.start, end=trip.end,
                            description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'No car with id = {car_id}'
        )




if __name__=='__main__':
    uvicorn.run('carsharing:app', reload=True)    
