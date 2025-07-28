from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class Trailer(TruckyIndicatorHotkey):
    off_text = "Free"
    on_text = "Hitched"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_TRAILER_OFF
    on_icon = Icons.ACT_TRAILER_ON
    data_path = ["trailer_connected"]
    indicator_id = "trailer"
    indicator_label = "Trailer"
    hotkey_label = "Trailer Bound Key"
    hotkey_default = "T"
    hotkey_var = "trailer.hotkey"
    hotkey_text_var = "trailer.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_TRAILER_ON, Icons.ACT_TRAILER_OFF]