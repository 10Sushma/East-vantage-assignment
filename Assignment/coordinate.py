import requests
 
Key = "aAy9IudyK9Uypl9ksDBGEDaIDyDfJug6"

mainURL = f"http://www.mapquestapi.com/geocoding/v1/address?key={Key}&location="

def getCoordinates(streetAddress, city, state):
    mainCoordinate = f"{mainURL}{streetAddress},{city},{state}"
    r = requests.get(mainCoordinate)
    Data = r.json()["results"][0]
    locationData=Data["locations"][0]
    return locationData