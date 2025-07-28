from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class HazardLights(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_HAZARD_OFF
    on_icon = Icons.ACT_HAZARD_OFF
    data_path = ["truck", "lights", "hazard_warning"]
    indicator_id = "hazard_lights"
    indicator_label = "Hazard Lights"
    hotkey_label = "Hazard Lights Bound Key"
    hotkey_default = "F"
    hotkey_var = "lights.hazard_lights.hotkey"
    hotkey_text_var = "lights.hazard_lights.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_HAZARD_ON, Icons.ACT_HAZARD_OFF]
