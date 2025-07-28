from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons

class Engine(TruckyIndicatorHotkey):
    off_text = ""
    on_text = ""
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_ENGINE_START
    on_icon = Icons.ACT_ENGINE_STOP
    data_path = ["truck", "engine_enabled"]
    indicator_id = "engine_enabled"
    indicator_label = "Engine Start"
    hotkey_label = "Engine Start Bound Key"
    hotkey_default = "E"
    hotkey_var = "engine_start.hotkey"
    hotkey_text_var = "engine_start.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_ENGINE_START, Icons.ACT_ENGINE_STOP]
