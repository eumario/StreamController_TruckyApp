from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class ParkingBrake(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_PARKING_BRAKE_OFF
    on_icon = Icons.ACT_PARKING_BRAKE_OFF
    data_path = ["truck", "parking_brake"]
    indicator_id = "parking_brake"
    indicator_label = "Parking Brake"
    hotkey_label = "Parking Brake Bound Key"
    hotkey_default = "SPACE"
    hotkey_var = "lights.parking_brake.hotkey"
    hotkey_text_var = "lights.parking_brake.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_PARKING_BRAKE_ON, Icons.ACT_PARKING_BRAKE_OFF]
