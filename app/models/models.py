import sys
import os

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.database import Base

# 중간 테이블 정의
order_topping_association = Table(
    "order_topping",
    Base.metadata,
    Column("order_id", ForeignKey("order.id"), primary_key=True),
    Column("topping_id", ForeignKey("topping.id"), primary_key=True),
)

order_consumable_association = Table(
    "order_consumable",
    Base.metadata,
    Column("order_id", ForeignKey("order.id"), primary_key=True),
    Column("consumable_id", ForeignKey("consumable.id"), primary_key=True),
)


class IceCream(Base):
    __tablename__ = "ice_cream"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<IceCream(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})>"


class Topping(Base):
    __tablename__ = "topping"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Topping(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})>"


class Consumable(Base):
    __tablename__ = "consumable"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Consumable(id={self.id}, name={self.name}, price={self.price}, quantity={self.quantity})>"


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    ice_cream_id = Column(Integer, ForeignKey("ice_cream.id", ondelete="CASCADE"))
    order_time = Column(DateTime(timezone=True), server_default=func.now())

    ice_cream = relationship("IceCream")
    toppings = relationship("Topping", secondary=order_topping_association)
    consumables = relationship("Consumable", secondary=order_consumable_association)

    def __repr__(self):
        return f"<Order(id={self.id}, ice_cream_id={self.ice_cream_id}, order_time={self.order_time})>"


class RobotLog(Base):
    __tablename__ = "robot_log"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, nullable=False)
    log_time = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<RobotLog(id={self.id}, status={self.status}, log_time={self.log_time})>"

class Table(Base):
    __tablename__ = "table"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer, default=1, nullable=False)
    
    def __repr__(self):
        return f"<Table(id={self.id}, status={self.status})>"