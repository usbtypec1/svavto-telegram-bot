from datetime import datetime

from pydantic import BaseModel

from enums import PenaltyConsequence, PenaltyReason
from models.staff import Staff

__all__ = ('Penalty',)


class Penalty(BaseModel):
    id: int
    staff: Staff
    reason: PenaltyReason | str
    amount: int
    consequence: PenaltyConsequence | None
    created_at: datetime
