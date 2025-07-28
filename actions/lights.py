from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class Lights(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_LIGHTS_OFF
    on_icon = Icons.ACT_LIGHTS_ON
    data_path = ["truck", "lights", "low_beam"]
    indicator_id = "low_beam"
    indicator_label = "Lights"
    hotkey_label = "Lights Bound Key"
    hotkey_default = "L"
    hotkey_var = "lights.low_beam.hotkey"
    hotkey_text_var = "lights.low_beam.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_LIGHTS_ON, Icons.ACT_LIGHTS_OFF]
