from datetime import datetime

from pydantic import BaseModel

__all__ = ('Surcharge',)


class Surcharge(BaseModel):
    id: int
    staff_id: int
    reason: str
    amount: int
    created_at: datetime
