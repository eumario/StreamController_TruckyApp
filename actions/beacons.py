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

class Beacons(TruckyIndicatorHotkey):
    off_text = "Off"
    on_text = "On"
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_BEACON_OFF
    on_icon = Icons.ACT_BEACON_ON
    data_path = ["truck", "lights", "beacons"]
    indicator_id = "beacons"
    indicator_label = "Light Beacons"
    hotkey_label = "Light Beacons Bound Key"
    hotkey_default = "O"
    hotkey_var = "beacons.hotkey"
    hotkey_text_var = "beacons.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_BEACON_ON, Icons.ACT_BEACON_OFF]
