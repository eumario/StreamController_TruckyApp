from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class Retarder(TruckyIndicatorHotkey):
    off_text = ""
    on_text = ""
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_CRUISE_CONTROL_OFF
    on_icon = Icons.ACT_CRUISE_CONTROL_ON
    data_path = ["truck", "retarder_level"]
    indicator_id = "retarder"
    indicator_label = "Retarder"
    hotkey_label = "Retarder Bound Key"
    hotkey_default = ";"
    hotkey_var = "lights.hazard_lights.hotkey"
    hotkey_text_var = "lights.hazard_lights.label"
    show_label_title = "Show Speed"
    show_label_subtitle = "When engaged, show speed of Cruise Control"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_CRUISE_CONTROL_ON, Icons.ACT_CRUISE_CONTROL_OFF]

    def is_on(self, data):
        retarder = data["truck"]["retarder_level"]
        return retarder > 0

    async def on_telemetry_update(self, event, data: dict):
        value = data["truck"]["retarder_"]
        self.on_text = f"Level {value}"
        await super().on_telemetry_update(event, data)