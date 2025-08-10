from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons
from loguru import logger as log

class CruiseControl(TruckyIndicatorHotkey):
    off_text = ""
    on_text = ""
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_CRUISE_CONTROL_OFF
    on_icon = Icons.ACT_CRUISE_CONTROL_ON
    data_path = ["truck", "cruise_control"]
    indicator_id = "hazard_lights"
    indicator_label = "Hazard Lights"
    hotkey_label = "Hazard Lights Bound Key"
    hotkey_default = "C"
    hotkey_var = "lights.hazard_lights.hotkey"
    hotkey_text_var = "lights.hazard_lights.label"
    show_label_title = "Show Speed"
    show_label_subtitle = "When engaged, show speed of Cruise Control"
    last_speed = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_CRUISE_CONTROL_ON, Icons.ACT_CRUISE_CONTROL_OFF]

    def is_on(self, data):
        speed = data["truck"]["cruise_control_converted"]
        return speed > 0

    def on_telemetry_update(self, event, data: dict):
        value = data["truck"]["cruise_control_converted"]
        if self.last_speed == value:
            return

        self.last_speed = value

        if value > 0:
            self.icon_name = self.on_icon
            self.on_text = value
            if self._show_label.get_value():
                self.set_bottom_label(self.on_text, color=self.on_color)
        else:
            self.icon_name = self.off_icon
            if self._show_label.get_value():
                self.set_bottom_label(self.off_text, color=self.off_color)

        self.current_icon = self.get_icon(self.icon_name)
        self.display_icon()