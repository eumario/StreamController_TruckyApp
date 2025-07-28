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

class DamageOptions(Enum):
    TRUCK = SimpleComboRowItem("truck", "Truck")
    TRAILER = SimpleComboRowItem("trailer", "Trailer")
    CARGO = SimpleComboRowItem("cargo", "Cargo")

class Damage(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["navigation", "distance_converted"]
        self.units = ["units", "distance"]
        self.icon_keys = [Icons.ACT_ATS_TRUCK, Icons.ACT_ETS2_TRUCK, Icons.ACT_TRAILER_DAMAGE, Icons.ACT_CARGO_DAMAGE]
        self.icon_name = Icons.ACT_ATS_TRUCK
        self.truck_icon_key = Icons.ACT_ATS_TRUCK
        self.current_icon = self.get_icon(Icons.ACT_ATS_TRUCK)
        self.text_color = [255, 255, 255, 255]
        self.last_game = ""

    def create_generative_ui(self):
        self._damage_options = ComboRow(
            action_core=self,
            var_name="damage.mode",
            default_value=DamageOptions.TRUCK.value,
            title="Display Damage",
            subtitle="Display damage for a specific part",
            complex_var_name=True,
            items=[
                DamageOptions.TRUCK.value,
                DamageOptions.TRAILER.value,
                DamageOptions.CARGO.value
            ],
            on_change=self._handle_damage_display_mode
        )

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self._damage_options.widget]

    def create_event_assigners(self):
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="switch-dam-display-mode",
                ui_label="Switch Nav Mode",
                default_event=Input.Key.Events.DOWN,
                callback=self._switch_display_mode
            )
        )

    async def on_telemetry_update(self, event, data: dict):
        if self.last_game != data["game"]["code"]:
            self.last_game = data["game"]["code"]
            if self.last_game == "ETS2":
                self.truck_icon_key = Icons.ACT_ETS2_TRUCK
            else:
                self.truck_icon_key = Icons.ACT_ATS_TRUCK

        damage = 0
        option = self._damage_options.get_selected_item().get_value()
        if option == "truck":
            damage = self.get_from_path(data)
            self.icon_name = self.truck_icon_key
        else:
            if option == "trailer":
                self.icon_name = Icons.ACT_TRAILER_DAMAGE
            else:
                self.icon_name = Icons.ACT_CARGO_DAMAGE
            trailers = self.get_from_path(data)
            if trailers:
                for t in trailers:
                    if option == "trailer":
                        damage += t["wear"]["chassis"]
                    else:
                        damage += t["cargo_damage"]
        self.current_icon = self.get_icon(self.icon_name)
        self.display_icon()
        if self.last_state == damage:
            return

        self.display_icon()
        self.last_state = damage
        damage *= 100
        damage = int(damage)
        self.display_text(f"{damage}%", "top")

    def _switch_display_mode(self, _):
        item = self._damage_options.get_selected_item()
        if item.get_value() == "cargo":
            self._damage_options.set_selected_item(DamageOptions.TRUCK.value)
            self._handle_damage_display_mode(None, DamageOptions.TRUCK.value, None)
        elif item.get_value() == "truck":
            self._damage_options.set_selected_item(DamageOptions.TRAILER.value)
            self._handle_damage_display_mode(None, DamageOptions.TRAILER.value, None)
        else:
            self._damage_options.set_selected_item(DamageOptions.CARGO.value)
            self._handle_damage_display_mode(None, DamageOptions.CARGO.value, None)

    def _handle_damage_display_mode(self, _, new: SimpleComboRowItem, __):
        id = new.get_value()
        if id == "truck":
            self.icon_name = self.truck_icon_key
        elif id == "trailer" or id == "cargo":
            self.data_path = ["trailers"]
            if id == "trailer":
                self.icon_name = Icons.ACT_TRAILER_DAMAGE
            else:
                self.icon_name = Icons.ACT_CARGO_DAMAGE

        self.current_icon = self.get_icon(self.icon_name)
        self.display_icon()