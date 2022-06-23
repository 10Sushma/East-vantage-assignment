import requests

# using mapquest api for getting the coordinate of perticuller address 

# api Secret Key  
Key = "aAy9IudyK9Uypl9ksDBGEDaIDyDfJug6"

mainURL = f"http://www.mapquestapi.com/geocoding/v1/address?key={Key}&location="

# it's return the address information along with coordinate of and address 
# It's take 3 parameter and use them as location query for api 

def getCoordinates(streetAddress, city, state):
    mainCoordinate = f"{mainURL}{streetAddress},{city},{state}"
    r = requests.get(mainCoordinate)
    Data = r.json()["results"][0]
    locationData=Data["locations"][0]
    return locationData