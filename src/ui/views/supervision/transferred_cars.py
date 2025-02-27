from models import ShiftCarsCountByStaff
from ui.views import TextView


class SupervisionTransferredCarsView(TextView):

    def __init__(self, shift_cars: ShiftCarsCountByStaff):
        self.__shift_cars = shift_cars

    def get_text(self) -> str:
        lines: list[str] = [
            f'<b>📆 Смена {self.__shift_cars.date:%d.%m.%Y}</b>',
        ]

        if self.__shift_cars.active_shifts:
            lines.append('\nВ смене:')

        for staff_cars in self.__shift_cars.active_shifts:
            lines.append(
                f'📍 {staff_cars.staff_full_name}: {staff_cars.cars_count} авто'
            )

        if self.__shift_cars.completed_shifts:
            lines.append('\nЗавершили смену:')
        for staff_cars in self.__shift_cars.completed_shifts:
            lines.append(
                f'📍 {staff_cars.staff_full_name} - {staff_cars.cars_count} авто'
            )

        if not any((
                self.__shift_cars.completed_shifts,
                self.__shift_cars.active_shifts,
        )):
            lines.append('😔 Нет добавленных авто')
        return '\n'.join(lines)
