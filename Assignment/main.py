from fastapi import FastAPI
from requests import delete
from . import schemas, models
from .adressdb import engine, SessionLocal 
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends,status,Response, HTTPException
from .coordinate import getCoordinates
from geopy.distance import geodesic

models.Base.metadata.create_all(engine)
app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    

app=FastAPI()

@app.post('/postAddress',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Address, db:Session=Depends(get_db)):
 
    streetAddress=request.streetAddress
    city=request.city
    state=request.state
    pincode=request.pincode
    country=request.country
    
    locationData = getCoordinates(streetAddress, city, state)
    new_adress=models.Address(
            streetAddress = streetAddress,
            city = city,
            state = state,
            country = country,
            pincode = pincode,
            longitude =  locationData["latLng"]["lng"],
            latitude =  locationData["latLng"]["lat"],
            mapUrl = locationData["mapUrl"]
    )
    db.add(new_adress)
    db.commit()
    db.refresh(new_adress)
    return new_adress


@app.get('/getAddress',status_code=status.HTTP_200_OK)
def getAddress( db:Session=Depends(get_db)):
    allAddress=db.query(models.Address).all()
    return allAddress


@app.put('/updateAdress/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request:schemas.Address, db: Session=Depends(get_db)) :
    streetAddress = request.streetAddress
    city = request.city
    state = request.state
    pincode = request.pincode
    country=request.country

    locationData = getCoordinates(streetAddress, city, state)

    updateAddress = {
        "streetAddress" : streetAddress,
        "city" : city,
        "state" : state,
        "country":country,   
        "pincode" : pincode,
        "longitude" :  locationData["latLng"]["lng"],
        "latitude" :  locationData["latLng"]["lat"],
        "mapUrl" : locationData["mapUrl"]
    }
    address=db.query(models.Address).filter(models.Address.id==id).update(updateAddress)

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Address with id {id} is not avaiable')
    
    db.commit()  
    return address

@app.delete('/deleteAdress/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session=Depends(get_db)):
    
    deletedAdress=db.query(models.Address).filter(models.Address.id==id).delete(synchronize_session=False)
    if not deletedAdress:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Address with id {id} is not avaiable')
   
   
    db.commit()
    return 'deleted'


@app.get("/readNearestAddress", status_code=status.HTTP_200_OK)
def getNearestAddress(res: Response, addressLine, city, state, db :Session = Depends(get_db)): 
        locationData = getCoordinates(addressLine, city, state)
        quaryCoordinate = locationData["latLng"]
        firstCoordinate = (quaryCoordinate["lat"] , quaryCoordinate["lng"])
        allAddress = db.query(models.Address).all()
        
        nearestAddress = []

        for i in allAddress:
            secondCoordinate = (i.latitude, i.longitude)
            distanceBetween = geodesic(firstCoordinate, secondCoordinate).km
            if distanceBetween <= 50:
                nearestAddress.append(i)
        
        return nearestAddress
