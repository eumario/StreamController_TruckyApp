from enum import StrEnum, Enum
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from GtkHelper.ComboRow import SimpleComboRowItem
from GtkHelper.GenerativeUI.ComboRow import ComboRow
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

class Gear(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["truck", "calculated_gear"]
        self.icon_keys = [Icons.ACT_GEAR]
        self.icon_name = Icons.ACT_GEAR
        self.current_icon = self.get_icon(Icons.ACT_GEAR)
        self.text_color = [255, 255, 255, 255]
        self.has_configuration = False
        self.last_state = "N"

    def on_ready(self):
        super().on_ready()

        self.display_text(self.last_state, "center")

    async def on_telemetry_update(self, event, data: dict):
        gear = self.get_from_path(data)

        if self.last_state == gear:
            return

        self.last_state = gear
        self.display_text(gear, "center")