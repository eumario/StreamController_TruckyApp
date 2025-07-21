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

class RightTurnIndicator(TruckyIndicatorHotkey):
    off_text = ""
    on_text = ""
    off_color = [255, 255, 255, 255]
    on_color = [0, 255, 0, 255]
    off_icon = Icons.ACT_RIGHT_TURN_OFF
    on_icon = Icons.ACT_RIGHT_TURN_ON
    data_path = ["truck", "lights", "rblinker_light"]
    indicator_id = "rblinker"
    indicator_label = "Right Turn"
    hotkey_label = "Right Turn Bound Key"
    hotkey_default = "]"
    hotkey_var = "lights.rblinker.hotkey"
    hotkey_text_var = "lights.rblinker.label"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_keys = [Icons.ACT_RIGHT_TURN_OFF, Icons.ACT_RIGHT_TURN_ON]
