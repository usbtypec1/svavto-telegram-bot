import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from enums import CarClass, WashType

__all__ = (
    'CarToWashWebAppData',
    'AdditionalService',
    'Car',
    'CarAdditionalServices',
    'ShiftCarsCountByStaff',
    'CarStatisticsItem',
    'ShiftCarsWithoutWindshieldWasher',
    'CarToWashCreateResult',
)


class AdditionalService(BaseModel):
    id: UUID
    count: int


class CarToWashWebAppData(BaseModel):
    number: str
    class_type: CarClass
    wash_type: WashType
    windshield_washer_refilled_bottle_percentage: int
    additional_services: list[AdditionalService] = Field(default_factory=list)


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
    additional_services: list[AdditionalService]


class CarStatisticsItem(BaseModel):
    staff_id: int
    staff_full_name: str
    cars_count: int


class ShiftCarsCountByStaff(BaseModel):
    date: datetime.date
    cars: list[CarStatisticsItem]


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
