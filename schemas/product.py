from pydantic import BaseModel


class Product(BaseModel):
    name: str
    quan: int
    class Config:
        orm_mode = True