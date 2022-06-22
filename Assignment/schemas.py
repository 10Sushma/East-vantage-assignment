from pydantic import BaseModel
class Address(BaseModel):
    streetAddress: str 
    city: str 
    state: str
    pincode: int
    country:str