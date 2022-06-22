from operator import index
from sqlalchemy import  Column,  Integer, String,Float
from .adressdb import Base

class Address(Base):
    __tablename__='addressBook'
    
    id=Column(Integer,primary_key=True,index=True)
    streetAddress=Column(String)
    city=Column(String)
    state=Column(String)
    country=Column(String)
    pincode=Column(Integer)
    longitude=Column(Float)
    latitude=Column(Float)
    mapUrl=Column(String)