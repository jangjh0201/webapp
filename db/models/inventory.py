from sqlalchemy import Column, Integer, ForeignKey
from .. import Base

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, index=True)
    item_type_id = Column(Integer, ForeignKey('item_type.id'), nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
