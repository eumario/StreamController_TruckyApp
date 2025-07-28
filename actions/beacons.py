from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class Beacons(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_BEACON_OFF
    on_icon = Icons.ACT_BEACON_ON
    data_path = ["truck", "lights", "beacons"]
    indicator_id = "beacons"
    indicator_label = "Light Beacons"
    hotkey_label = "Light Beacons Bound Key"
    hotkey_default = "O"
    hotkey_var = "beacons.hotkey"
    hotkey_text_var = "beacons.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_BEACON_ON, Icons.ACT_BEACON_OFF]
