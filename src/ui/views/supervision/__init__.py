from .dead_souls import DeadSoulsMonthChooseView, DeadSoulsView
from .menu import SupervisionMenuView
from .shift_confirmations import SupervisionShiftConfirmationsView
from .transferred_cars import SupervisionTransferredCarsView
from .windshield_washer import SupervisionWindshieldWasherView


__all__ = (
    'SupervisionMenuView',
    'DeadSoulsView',
    'SupervisionWindshieldWasherView',
    'SupervisionShiftConfirmationsView',
    'SupervisionTransferredCarsView',
    'DeadSoulsMonthChooseView'
)
