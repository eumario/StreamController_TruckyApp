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



class SpeedText(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["truck", "speed_converted"]
        self.color_keys = [Colors.NONE, Colors.WARNING, Colors.ALERT]
        self.color_name = Colors.NONE
        self.last_limit = 0
        self.has_configuration = True

    async def on_telemetry_update(self, event, data: dict):
        speed = data["truck"]["speed_converted"]
        limit = self.get_from_specific_path(["navigation", "speed_limit_converted"], data)

        if self.last_state == speed and self.last_limit == limit:
            return
        self.last_state = speed
        self.last_limit = limit
        unit = self.get_from_specific_path(["units", "speed"], data)

        diff = limit - speed

        colorize = self._show_speed_warning.get_active()
        if colorize:
            if diff >= 0:
                self.color_name = Colors.NONE
            elif 0 > diff >= -2:
                self.color_name = Colors.WARNING
            elif 0 > diff > -2:
                self.color_name = Colors.ALERT
            self.current_color = self.get_color(self.color_name)
            self.display_color()
        self.set_center_label(str(speed), font_size=24)
        if self._show_speed_unit.get_active():
            self.set_bottom_label(data["units"]["speed"])

    def create_generative_ui(self):
        self._show_speed_unit = SwitchRow(
            action_core=self,
            var_name="speed.show_unit",
            default_value=True,
            title="Show Unit",
            subtitle="Shows the Speed Unit based on game",
            complex_var_name=True
        )
        self._show_speed_warning = SwitchRow(
            action_core=self,
            var_name="speed.show_warning",
            default_value=True,
            title="Show Warning",
            subtitle="Colors speed based on Speed Limit",
            complex_var_name=True
        )

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self._show_speed_unit.widget, self._show_speed_warning.widget]