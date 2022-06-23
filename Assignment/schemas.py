from pydantic import BaseModel

#  create Pydantic schemas that will be used when reading data, when returning it from the API
class Address(BaseModel):
    streetAddress: str 
    city: str 
    state: str
    pincode: int
    country:str