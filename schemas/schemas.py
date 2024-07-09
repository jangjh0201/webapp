from pydantic import BaseModel
from typing import List, Optional


class IceCreamBase(BaseModel):
    name: str
    price: int


class IceCreamCreate(IceCreamBase):
    pass


class IceCream(IceCreamBase):
    id: int

    class Config:
        from_attributes = True


class ToppingBase(BaseModel):
    name: str
    price: int


class ToppingCreate(ToppingBase):
    pass


class Topping(ToppingBase):
    id: int

    class Config:
        from_attributes = True


class OtherItemBase(BaseModel):
    name: str
    price: int


class OtherItemCreate(OtherItemBase):
    pass


class OtherItem(OtherItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    ice_cream_id: int
    other_item_ids: List[int]
    toppings: Optional[List[int]] = None


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True


class InventoryBase(BaseModel):
    item_type: str
    item_id: int
    quantity: int


class InventoryCreate(InventoryBase):
    pass


class Inventory(InventoryBase):
    id: int

    class Config:
        from_attributes = True
