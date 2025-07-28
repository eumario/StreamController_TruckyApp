from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class LeftTurnIndicator(TruckyIndicatorHotkey):
    off_text = ""
    on_text = ""
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_LEFT_TURN_OFF
    on_icon = Icons.ACT_LEFT_TURN_ON
    data_path = ["truck", "lights", "lblinker_light"]
    indicator_id = "lblinker"
    indicator_label = "Left Turn"
    hotkey_label = "Left Turn Bound Key"
    hotkey_default = "["
    hotkey_var = "lights.lblinker.hotkey"
    hotkey_text_var = "lights.lblinker.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_LEFT_TURN_OFF, Icons.ACT_LEFT_TURN_ON]
