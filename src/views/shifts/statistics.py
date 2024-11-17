from models import ShiftCarsCountByStaff, ShiftCarsWithoutWindshieldWasher
from views.base import TextView

__all__ = (
    'ShiftCarsWithoutWindshieldWasherView',
    'ShiftCarsCountByStaffView',
)


class ShiftCarsWithoutWindshieldWasherView(TextView):

    def __init__(self, shift_cars: ShiftCarsWithoutWindshieldWasher):
        self.__shift_cars = shift_cars

    def get_text(self) -> str:
        lines: list[str] = [
            f'<b>Смена {self.__shift_cars.date:%d.%m.%Y}</b>',
        ]
        if not self.__shift_cars.cars:
            lines.append('Пока нет авто с недоливами')
        for car_number in self.__shift_cars.cars:
            lines.append(car_number)

        return '\n'.join(lines)


class ShiftCarsCountByStaffView(TextView):

    def __init__(self, shift_cars: ShiftCarsCountByStaff):
        self.__shift_cars = shift_cars

    def get_text(self) -> str:
        lines: list[str] = [
            f'<b>Смена {self.__shift_cars.date:%d.%m.%Y}</b>',
        ]
        if not self.__shift_cars.cars:
            lines.append('Пока нет внесенных авто')
        for position, item in enumerate(
                self.__shift_cars.cars,
                start=1,
        ):
            lines.append(
                f'{position}. {item.staff_full_name} - {item.cars_count} авто'
            )

        return '\n'.join(lines)
