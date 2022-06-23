from fastapi import FastAPI
from . import schemas, models
from .adressdb import engine, SessionLocal 
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends,status,Response, HTTPException
from .coordinate import getCoordinates
from geopy.distance import geodesic

models.Base.metadata.create_all(engine)
app=FastAPI()

# Dependency
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    

app=FastAPI()


#  creating an address from request body 
@app.post('/postAddress',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Address, db:Session=Depends(get_db)):
 
    streetAddress=request.streetAddress
    city=request.city
    state=request.state
    pincode=request.pincode
    country=request.country
    
    # getting the location & coordinate data from mapquest api 
    locationData = getCoordinates(streetAddress, city, state)
    
    # creaing new row for address table 
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
    db.add(new_adress) #add that instance object to database session
    db.commit() # commit the changes to the database 
    db.refresh(new_adress)# refresh the instance
    return new_adress 

# get all adress
@app.get('/getAddress',status_code=status.HTTP_200_OK)
def getAddress( db:Session=Depends(get_db)):
    
    # get all the address data from  database and return to user 
    allAddress=db.query(models.Address).all()
    return allAddress

# update the address through id and request body 
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
     # updating address through id and query params
    address=db.query(models.Address).filter(models.Address.id==id).update(updateAddress)
    
    #if data not found in database raise the status code and details
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Address with id {id} is not avaiable')
    
    db.commit()  
    return address

# delete addresses
@app.delete('/deleteAdress/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db: Session=Depends(get_db)):
    
    deletedAdress=db.query(models.Address).filter(models.Address.id==id).delete(synchronize_session=False)
    
    #ifdata not found in database raise the status code and details
    if not deletedAdress:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Address with id {id} is not avaiable')
   
    db.commit()
    return 'deleted'

# retrieve the addresses that are within a given distance and location coordinates.
@app.get("/getNearestAddress", status_code=status.HTTP_200_OK)
def getNearestAddress(res: Response, streetAddress, city, state, db :Session = Depends(get_db)): 
    
        locationData = getCoordinates(streetAddress, city, state)
        
        data = locationData["latLng"]
        origin = (data["lat"] , data["lng"])
        allAddress = db.query(models.Address).all()       
        
        nearestAddress = []
        for i in allAddress:
            dist = (i.latitude, i.longitude)
            
            # geodesic is importaed from geopy.distance module
            #  In here geodesic returning the distance between given address and all database address,
            distanceBetween = geodesic(origin, dist).km
            
            # If the distance is below 50km than only it's save the address to nearstAddress list. 
            if distanceBetween <= 50:
                
                # Here, nearestAddress will hold all the address that between 50km
                nearestAddress.append(i)
                
        # # return the nearest address data to user
        return nearestAddress
