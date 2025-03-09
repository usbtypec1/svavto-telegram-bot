import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from enums import CarClass, WashType


__all__ = (
    'CarToWashWebAppData',
    'AdditionalService',
    'Car',
    'CarAdditionalServices',
    'ShiftCarsCountByStaff',
    'CarCountTransferredByStaff',
    'ShiftCarsWithoutWindshieldWasher',
    'CarToWashCreateResult',
    'TransferredCarsListResponse',
    'TransferredCarsListItem',
    'TransferredCarAdditionalService',
)


class AdditionalService(BaseModel):
    id: UUID
    count: int


class CarToWashWebAppData(BaseModel):
    number: str
    class_type: CarClass
    wash_type: WashType
    windshield_washer_refilled_bottle_percentage: int
    additional_services: Annotated[
        list[AdditionalService],
        Field(default_factory=list),
    ]


class Car(BaseModel):
    id: int
    number: str
    car_class: CarClass
    wash_type: WashType
    windshield_washer_refilled_bottle_percentage: int
    created_at: datetime.datetime
    additional_services: list[AdditionalService]


class CarAdditionalServices(BaseModel):
    id: int
    windshield_washer_refilled_bottle_percentage: int
    additional_services: list[AdditionalService]


class CarCountTransferredByStaff(BaseModel):
    staff_id: int
    staff_full_name: str
    cars_count: int


class ShiftCarsCountByStaff(BaseModel):
    date: datetime.date
    active_shifts: list[CarCountTransferredByStaff]
    completed_shifts: list[CarCountTransferredByStaff]


class ShiftCarsWithoutWindshieldWasher(BaseModel):
    date: datetime.date
    cars: list[str]


class CarToWashCreateResult(BaseModel):
    id: int
    shift_id: int
    number: str
    class_type: CarClass
    wash_type: WashType
    windshield_washer_refilled_bottle_percentage: int
    car_wash_id: int
    additional_services: list[AdditionalService]


class TransferredCarAdditionalService(BaseModel):
    id: UUID
    name: str
    count: int


class TransferredCarsListItem(BaseModel):
    id: int
    number: str
    class_type: CarClass
    wash_type: WashType
    car_wash_id: int
    car_wash_name: str
    windshield_washer_refilled_bottle_percentage: int
    additional_services: list[TransferredCarAdditionalService]


class TransferredCarsListResponse(BaseModel):
    shift_id: int
    shift_date: datetime.date
    staff_id: int
    staff_full_name: str
    transferred_cars: list[TransferredCarsListItem]
