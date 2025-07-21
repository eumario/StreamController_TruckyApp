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

class ParkingBrake(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_PARKING_BRAKE_OFF
    on_icon = Icons.ACT_PARKING_BRAKE_OFF
    data_path = ["truck", "parking_brake"]
    indicator_id = "parking_brake"
    indicator_label = "Parking Brake"
    hotkey_label = "Parking Brake Bound Key"
    hotkey_default = "SPACE"
    hotkey_var = "lights.parking_brake.hotkey"
    hotkey_text_var = "lights.parking_brake.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_PARKING_BRAKE_ON, Icons.ACT_PARKING_BRAKE_OFF]
