from datetime import datetime

from pydantic import BaseModel

__all__ = ('Penalty',)


class Penalty(BaseModel):
    id: int
    staff_id: int
    reason: str
    created_at: datetime
    is_notification_delivered: bool
