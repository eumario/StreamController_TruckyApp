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

class FuelOptions(Enum):
    VOLUME = SimpleComboRowItem("volume", "Fuel Volume")
    DISTANCE = SimpleComboRowItem("distance", "Fuel Distance")

class Fuel(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["truck", "fuel_converted"]
        self.units = ["units", "volume"]
        self.icon_keys = [Icons.ACT_FUEL]
        self.icon_name = Icons.ACT_FUEL
        self.current_icon = self.get_icon(Icons.ACT_FUEL)
        self.text_color = [255, 255, 255, 255]


    def create_generative_ui(self):
        self._fuel_display_mode = ComboRow(
            action_core=self,
            var_name="fuel.mode",
            default_value=FuelOptions.VOLUME.value,
            title="Fuel Display",
            subtitle="Mode in which to Display Fuel Tanks",
            complex_var_name=True,
            items=[
                FuelOptions.VOLUME.value,
                FuelOptions.DISTANCE.value
            ],
            on_change=self._handle_fuel_display_mode
        )

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self._fuel_display_mode.widget]

    async def on_telemetry_update(self, event, data: dict):
        fuel = self.get_from_path(data)
        if self.last_state == fuel:
            return

        units = self.get_from_specific_path(self.units, data)

        self.last_state = fuel
        self.display_text(f"{fuel} {units}", "top")

    def _handle_fuel_display_mode(self, _, new: SimpleComboRowItem, __):
        id: str = new.get_value()
        if id == "volume":
            self.data_path[1] = "fuel_converted"
            self.units[1] = "volume"
        else:
            self.data_path[1] = "fuel_range_converted"
            self.units[1] = "distance"

        self.display_text("", "bottom")