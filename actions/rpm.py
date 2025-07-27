from enum import StrEnum, Enum
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from GtkHelper.GenerativeUI.SwitchRow import SwitchRow
from .trucky_core import TruckyCore
from .trucky_indicator_display import TruckyIndicatorDisplay
from ..globals import Icons
from ..globals import Colors
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input
from src.backend.PluginManager.PluginSettings.Asset import Color

from loguru import logger as log

from gi.repository import Gtk, Adw
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class Rpm(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["truck", "fuel_converted"]
        self.has_configuration = False
        self.icon_keys = [Icons.ACT_RPM]
        self.text_color = [255,255,255,255]
        self.current_icon = self.get_icon(Icons.ACT_RPM)

    async def on_telemetry_update(self, event, data: dict):
        rpm = self.get_from_path(data)
        if self.last_state == rpm:
            return

        self.last_state = rpm
        self.display_text(rpm, "bottom")
