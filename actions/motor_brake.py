from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class MotorBrake(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_MOTOR_BRAKE_OFF
    on_icon = Icons.ACT_MOTOR_BRAKE_ON
    data_path = ["truck", "motor_brake"]
    indicator_id = "motor_brake"
    indicator_label = "Motor Brake"
    hotkey_label = "Motor Brake Bound Key"
    hotkey_default = "B"
    hotkey_var = "motor_brake.hotkey"
    hotkey_text_var = "motor_brake.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_MOTOR_BRAKE_ON, Icons.ACT_MOTOR_BRAKE_OFF]
