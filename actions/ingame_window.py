from enum import Enum
from GtkHelper.ComboRow import SimpleComboRowItem
from GtkHelper.GenerativeUI.ComboRow import ComboRow
from .trucky_core import TruckyCore
from ..globals import Icons
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input

from gi.repository import Adw
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class InGameWindowOptions(Enum):
    DESKTOP_HELPER = SimpleComboRowItem("desktopHelper", "Desktop Helper")
    DESKTOP_WINDOW = SimpleComboRowItem("desktopWindow", "Desktop Window")
    GAME_INFO = SimpleComboRowItem("gameInfo", "Game info")
    DISPATCHER = SimpleComboRowItem("dispatcher", "Dispatcher")
    SETTINGS = SimpleComboRowItem("settings", "Settings")
    LIVE_MAP = SimpleComboRowItem("liveMap", "Live Map")
    SERVERS = SimpleComboRowItem("servers", "TruckersMP - Servers")
    TRAFFIC = SimpleComboRowItem("traffic", "TruckersMP - Traffic")
    ROUTE_HELPER = SimpleComboRowItem("routeHelper", "Public Transport - Route Helper")
    LINES_MANAGER = SimpleComboRowItem("linesManager", "Public Transport - Lines Manager")


class InGameWindow(TruckyCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.has_configuration = True

        self.icon_keys = [Icons.ACT_GAME_WIN]
        self.current_icon = self.get_icon(Icons.ACT_GAME_WIN)
        self.icon_name = Icons.ACT_GAME_WIN
        self.labels = {
            "desktopHelper": "Desktop Helper",
            "desktopWindow": "Desktop Window",
            "gameInfo": "Game Info",
            "dispatcher": "Dispatcher",
            "settings": "Settings",
            "liveMap": "Live Map",
            "servers": "Servers",
            "traffic": "Traffic",
            "routeHelper": "Route Helper",
            "linesManager": "Lines Manager"
        }

    def create_event_assigners(self):
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="ingame-window",
                ui_label="InGame Window",
                default_event=Input.Key.Events.DOWN,
                callback=self._show_window
            )
        )

    def create_generative_ui(self):
        self._ingame_window_shown = ComboRow(
            action_core=self,
            var_name="ingame.window",
            default_value=InGameWindowOptions.DESKTOP_HELPER.value,
            title="In-Game Window",
            subtitle="Select a Trucky Window to Show",
            complex_var_name=True,
            items=[
                InGameWindowOptions.DESKTOP_HELPER.value,
                InGameWindowOptions.DESKTOP_WINDOW.value,
                InGameWindowOptions.GAME_INFO.value,
                InGameWindowOptions.DISPATCHER.value,
                InGameWindowOptions.SETTINGS.value,
                InGameWindowOptions.LIVE_MAP.value,
                InGameWindowOptions.SERVERS.value,
                InGameWindowOptions.TRAFFIC.value,
                InGameWindowOptions.ROUTE_HELPER.value,
                InGameWindowOptions.LINES_MANAGER.value
            ],
            on_change=self._handle_window_changed
        )

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self._ingame_window_shown.widget]

    def _show_window(self, _):
        opt = self._ingame_window_shown.get_selected_item()
        self.backend.send_window(opt.get_value())

    def _handle_window_changed(self, _, new: SimpleComboRowItem, __):
        id: str = new.get_value()
        label = self.labels[id]
        if " " in label:
            top, bottom = label.split(" ")
            self.set_top_label(top)
            self.set_bottom_label(bottom)
        else:
            self.set_top_label("")
            self.set_bottom_label(label)