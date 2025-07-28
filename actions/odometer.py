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

class Odometer(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["truck", "odometer_converted"]
        self.units = ""
        self.icon_keys = [Icons.ACT_ODOMETER]
        self.icon_name = Icons.ACT_ODOMETER
        self.current_icon = self.get_icon(Icons.ACT_ODOMETER)
        self.text_color = [255, 255, 255, 255]
        self.has_configuration = False
        self.last_state = ""

    def on_ready(self):
        super().on_ready()

        self.display_text(self.last_state, "top")

    async def on_telemetry_update(self, event, data: dict):
        odo = self.get_from_path(data)

        if self.last_state == odo:
            return

        if self.units != data["units"]["distance"]:
            self.units = data["units"]["distance"]

        self.last_state = odo
        self.display_text(f"{odo:,d} {self.units}", "top")