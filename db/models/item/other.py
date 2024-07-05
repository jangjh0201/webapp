from sqlalchemy import Column, Integer, String
from .. import Base

class Other(Base):
    __tablename__ = 'other'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
