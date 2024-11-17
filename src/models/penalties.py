from datetime import datetime

from pydantic import BaseModel

from enums import PenaltyConsequence, PenaltyReason

__all__ = ('Penalty',)


class Penalty(BaseModel):
    id: int
    staff_id: int
    reason: PenaltyReason | str
    amount: int
    consequence: PenaltyConsequence | None
    created_at: datetime
