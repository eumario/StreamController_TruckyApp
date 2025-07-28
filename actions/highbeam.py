from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class HighBeam(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_HIGH_BEAM_OFF
    on_icon = Icons.ACT_HIGH_BEAM_ON
    data_path = ["truck", "lights", "high_beam"]
    indicator_id = "high_beam"
    indicator_label = "High Beams"
    hotkey_label = "High Beam Bound Key"
    hotkey_default = "K"
    hotkey_var = "lights.high_beam.hotkey"
    hotkey_text_var = "lights.high_beam.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_HIGH_BEAM_ON, Icons.ACT_HIGH_BEAM_OFF]
