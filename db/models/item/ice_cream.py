from sqlalchemy import Column, Integer, String
from .. import Base

class IceCream(Base):
    __tablename__ = 'ice_cream'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)