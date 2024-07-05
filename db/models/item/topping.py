from sqlalchemy import Column, Integer, String
from .. import Base

class Topping(Base):
    __tablename__ = 'topping'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
