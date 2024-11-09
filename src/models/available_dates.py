from pydantic import BaseModel

__all__ = ('AvailableDate',)


class AvailableDate(BaseModel):
    id: int
    month: int
    year: int
