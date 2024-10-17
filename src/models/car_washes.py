from pydantic import BaseModel

__all__ = ('CarWash',)


class CarWash(BaseModel):
    id: int
    name: str
