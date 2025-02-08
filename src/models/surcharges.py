import datetime

from pydantic import BaseModel

__all__ = ('Surcharge',)


class Surcharge(BaseModel):
    id: int
    staff_id: int
    staff_full_name: str
    shift_id: int
    shift_date: datetime.date
    reason: str
    amount: int
    created_at: datetime.datetime
