from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class Wipers(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_WIPERS_OFF
    on_icon = Icons.ACT_WIPERS_ON
    data_path = ["truck", "wipers"]
    indicator_id = "wipers"
    indicator_label = "Windshield Wipers"
    hotkey_label = "Windshield Wipers Bound Key"
    hotkey_default = "P"
    hotkey_var = "wipers.hotkey"
    hotkey_text_var = "wipers.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_WIPERS_ON, Icons.ACT_WIPERS_OFF]
