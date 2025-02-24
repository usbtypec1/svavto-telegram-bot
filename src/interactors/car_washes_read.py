from dataclasses import dataclass

from exceptions import NoAnyCarWashError
from models import CarWash
from repositories import CarWashRepository


@dataclass(frozen=True, slots=True)
class CarWashesReadInteractor:
    car_wash_repository: CarWashRepository

    async def execute(self) -> list[CarWash]:
        car_washes = await self.car_wash_repository.get_all()
        if not car_washes:
            raise NoAnyCarWashError
        return car_washes
