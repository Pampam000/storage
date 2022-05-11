from pydantic import BaseModel


class UserBase(BaseModel):

    login: str
    is_seller: bool


class UserCreate(UserBase):

    password: str


class User(UserBase):

    class Config:
        orm_mode = True