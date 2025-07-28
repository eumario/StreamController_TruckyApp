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

class SpeedLimit(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["navigation", "speed_limit_converted"]
        self.units = ""
        self.icon_keys = [Icons.ACT_ATS_SPEED_LIMIT, Icons.ACT_ETS2_SPEED_LIMIT]
        self.icon_name = Icons.ACT_ATS_SPEED_LIMIT
        self.current_icon = self.get_icon(Icons.ACT_ATS_SPEED_LIMIT)
        self.text_color = [0, 0, 0, 255]
        self.has_configuration = False
        self.last_state = 0
        self.last_game = ""

    def on_ready(self):
        super().on_ready()

        if self.last_state == 0:
            self.display_text("", "center")
        else:
            self.display_text(self.last_state, "center", 24)
        self.display_icon()

    async def on_telemetry_update(self, event, data: dict):
        if self.last_game != data["game"]["code"]:
            self.last_game = data["game"]["code"]
            if self.last_game == "ETS2":
                self.icon_name = Icons.ACT_ETS2_SPEED_LIMIT
            else:
                self.icon_name = Icons.ACT_ATS_SPEED_LIMIT
            self.current_icon = self.get_icon(self.icon_name)
            self.display_icon()

        limit = self.get_from_path(data)

        if self.last_state == limit:
            return

        self.last_state = limit
        if limit == 0:
            self.display_text("","center")
        else:
            self.display_text(f"{limit}", "center", 24, 0)