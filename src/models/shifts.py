from pydantic import BaseModel

__all__ = ('ShiftFinishResult',)


class ShiftFinishResult(BaseModel):
    is_first_shift: bool
    staff_full_name: str
    car_numbers: list[str]
