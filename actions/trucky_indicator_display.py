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

class TruckyIndicatorDisplay(TruckyCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def display_text(self, text, position: str = "bottom"):
        self.set_label(text=text, color=self.text_color, position=position)