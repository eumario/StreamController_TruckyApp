from enum import StrEnum, Enum
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from GtkHelper.GenerativeUI.EntryRow import EntryRow
from GtkHelper.GenerativeUI.SwitchRow import SwitchRow
from .trucky_core import TruckyCore
from .trucky_indicator_hotkey import TruckyIndicatorHotkey
from ..globals import Icons
from ..globals import Colors
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input
from src.backend.PluginManager.PluginSettings.Asset import Color

from loguru import logger as log

from gi.repository import Adw
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_CRUISE_CONTROL_ON, Icons.ACT_CRUISE_CONTROL_OFF]

    def is_on(self, data):
        speed = data["truck"]["cruise_control_converted"]
        return speed > 0

    async def on_telemetry_update(self, event, data: dict):
        value = data["truck"]["cruise_control_converted"]
        self.on_text = value
        await super().on_telemetry_update(event, data)