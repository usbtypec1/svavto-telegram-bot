import datetime

from ui.views.base import TextView


__all__ = (
    'ShiftExtraStartRequestRejectedView',
    'ShiftExtraStartRequestConfirmedView',
    'ShiftExtraStartRequestSentView',
)


class ShiftExtraStartRequestConfirmedView(TextView):
    """
    Staff receives this view
    after admin confirms their request to start an extra shift.
    """

    def __init__(
            self,
            staff_full_name: str,
            shift_date: datetime.date,
    ):
        self.__staff_full_name = staff_full_name
        self.__shift_date = shift_date

    def get_text(self) -> str:
        return (
            f'✅ {self.__staff_full_name}, ваш запрос на доп.смену на дату'
            f' {self.__shift_date:%d.%m.%Y} подтвержден.\n'
            'Вы сможете начать смену в разделе "начать смену"'
        )


class ShiftExtraStartRequestRejectedView(TextView):
    """
    Staff receives this view after their request for an extra shift is
    rejected.
    """

    def __init__(self, shift_date: datetime.date):
        self.__shift_date = shift_date

    def get_text(self) -> str:
        return (
            f'❌ Ваш запрос на доп.смену'
            f' {self.__shift_date:%d.%m.%Y} отклонен'
        )


class ShiftExtraStartRequestSentView(TextView):
    """
    Staff receives this view after they request for an extra shift
    """

    def __init__(self, shift_date: datetime.date):
        self.__shift_date = shift_date

    def get_text(self) -> str:
        return (
            '✅ Ваш запрос на доп.смену в'
            f' {self.__shift_date:%d.%m.%Y} отправлен на проверку'
        )
