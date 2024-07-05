from sqlalchemy import Column, Integer, String
from .. import Base

class ItemType(Base):
    __tablename__ = 'item_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
