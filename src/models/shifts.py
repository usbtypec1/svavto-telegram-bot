from pydantic import BaseModel

__all__ = ('ShiftFinishResult', 'ShiftConfirmation')


class ShiftFinishResult(BaseModel):
    is_first_shift: bool
    staff_full_name: str
    car_numbers: list[str]


class ShiftConfirmation(BaseModel):
    shift_id: int
    staff_id: int
    staff_full_name: str
