from datetime import datetime

from pydantic import BaseModel

__all__ = ('Performer',)


class Performer(BaseModel):
    id: int
    telegram_id: int
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str
    is_banned: bool
    created_at: datetime
