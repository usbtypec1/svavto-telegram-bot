from ui.views.base import TextView


__all__ = ('ShiftTodayStartInvalidTimeView',)


class ShiftTodayStartInvalidTimeView(TextView):
    text = (
        'До 21:30 Вам придет уведомление в этот бот с запросом'
        ' <b>подтвердить или отклонить</b> выход на смену.'
        '\nПосле подтверждения нажмите на кнопку "Начать смену"'
        ' и смена откроется.'
    )
