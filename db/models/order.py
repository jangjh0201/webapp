from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from .. import Base

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    ice_cream_id = Column(Integer, ForeignKey('ice_cream.id'))
    topping_id = Column(Integer, ForeignKey('topping.id'))
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    ice_cream = relationship('IceCream')
    topping = relationship('Topping')
