from pydantic import BaseModel

__all__ = ('ShiftFinishResult',)


class ShiftFinishResult(BaseModel):
    staff_full_name: str
    car_numbers: list[str]
