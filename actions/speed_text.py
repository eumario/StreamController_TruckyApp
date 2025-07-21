from enum import StrEnum, Enum
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from GtkHelper.GenerativeUI.SwitchRow import SwitchRow
from .trucky_core import TruckyCore
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



class SpeedText(TruckyCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True

    async def on_telemetry_update(self, event, data: dict):
        colorize = self._show_speed_warning.get_active()
        limit = data["navigation"]["speed_limit_converted"]
        speed = data["truck"]["speed_converted"]
        unit = data["units"]["speed"]
        color = self.get_color(Colors.NORMAL)
        if colorize:
            diff = limit - speed
            if diff < 0:
                if diff < -2:
                    color = self.get_color(Colors.ALERT)
                else:
                    color = self.get_color(Colors.WARNING)
            self.set_center_label(str(speed), font_size=24, color=color)
        else:
            self.set_center_label(str(speed), font_size=24, color=color)
        if self._show_speed_unit.get_active():
            self.set_bottom_label(data["units"]["speed"])

    def create_event_assigners(self):
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="speed-text",
                ui_label="Speed Text",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_key_down,
            )
        )

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

    def _on_key_down(self):
        pass