from ui.views.base import TextView


__all__ = ('ShiftNotConfirmedView',)


class ShiftNotConfirmedView(TextView):
    text = (
        'До начала смены Вам придет уведомление в этот бот с запросом'
        ' <b>подтвердить или отклонить</b> выход на смену.'
        '\nПосле подтверждения нажмите на кнопку "Начать смену"'
        ' и смена откроется.'
    )
