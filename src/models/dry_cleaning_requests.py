import datetime
from uuid import UUID

from pydantic import BaseModel

from enums import DryCleaningRequestStatus


class DryCleaningRequestService(BaseModel):
    id: UUID
    count: int


class DryCleaningRequestServiceWithName(DryCleaningRequestService):
    name: str


class DryCleaningRequest(BaseModel):
    id: int
    shift_id: int
    car_number: str
    photo_file_ids: list[str]
    services: list[DryCleaningRequestService]
    status: DryCleaningRequestStatus
    response_comment: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
