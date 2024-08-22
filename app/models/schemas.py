from pydantic import BaseModel
from typing import List, Optional


class IceCream(BaseModel):
    id: int
    name: str
    price: int
    quantity: int

    class Config:
        from_attributes = True


class Topping(BaseModel):
    id: int
    name: str
    price: int
    quantity: int

    class Config:
        from_attributes = True


class Consumable(BaseModel):
    id: int
    name: str
    price: int
    quantity: int

    class Config:
        from_attributes = True


class Order(BaseModel):
    id: int
    ice_cream_id: int
    topping_ids: Optional[List[int]] = None
    consumable_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True


class RobotLog(BaseModel):
    id: int
    status: int

    class Config:
        from_attributes = True


class User(BaseModel):
    username: str
    password: str

class Table(BaseModel):
    id: int

    class Config:
        from_attributes = True

FAKE_USERS_DB = {
    "addinedu": {
        "username": "addinedu",
        "password": "pinklab",  # 실제로는 해시된 비밀번호를 사용해야 합니다.
    }
}
