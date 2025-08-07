from .trucky_indicator_display import TruckyIndicatorDisplay
from ..globals import Icons

class Rpm(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["truck", "fuel_converted"]
        self.has_configuration = False
        self.icon_keys = [Icons.ACT_RPM]
        self.text_color = [255,255,255,255]
        self.current_icon = self.get_icon(Icons.ACT_RPM)

    def on_telemetry_update(self, event, data: dict):
        rpm = self.get_from_path(data)
        if self.last_state == rpm:
            return

        self.last_state = rpm
        self.display_text(rpm, "bottom")
