from pydantic import BaseModel

__all__ = ('Performer',)


class Performer(BaseModel):
    telegram_id: int
    full_name: str
    car_sharing_phone_number: str
    console_phone_number: str
