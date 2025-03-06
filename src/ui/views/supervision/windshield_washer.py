from models import ShiftCarsWithoutWindshieldWasher
from ui.views import TextView


class SupervisionWindshieldWasherView(TextView):

    def __init__(self, shift_cars: ShiftCarsWithoutWindshieldWasher):
        self.__shift_cars = shift_cars

    def get_text(self) -> str:
        lines: list[str] = [
            f'<b>💧 Недоливы. Смена {self.__shift_cars.date:%d.%m.%Y}</b>',
        ]
        if not self.__shift_cars.cars:
            lines.append('Пока нет авто с недоливами')
        for i, car_number in enumerate(self.__shift_cars.cars, start=1):
            lines.append(f'{i}. {car_number}')

        return '\n'.join(lines)
