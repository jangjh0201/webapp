from pydantic import BaseModel
from typing import List, Optional


class IceCreamBase(BaseModel):
    name: str
    price: int
    quantity: int


class IceCreamCreate(IceCreamBase):
    pass


class IceCream(IceCreamBase):
    id: int

    class Config:
        orm_mode = True


class ToppingBase(BaseModel):
    name: str
    price: int
    quantity: int


class ToppingCreate(ToppingBase):
    pass


class Topping(ToppingBase):
    id: int

    class Config:
        orm_mode = True


class ConsumableBase(BaseModel):
    name: str
    price: int
    quantity: int


class ConsumableCreate(ConsumableBase):
    pass


class Consumable(ConsumableBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    ice_cream_id: int
    toppings: Optional[List[int]] = None
    consumables: Optional[List[int]] = None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
