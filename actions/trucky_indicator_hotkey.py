from typing import Optional

from GtkHelper.GenerativeUI.EntryRow import EntryRow
from GtkHelper.GenerativeUI.SwitchRow import SwitchRow
from .trucky_core import TruckyCore
from ..globals import Icons
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input

from gi.repository import Adw
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class TruckyIndicatorHotkey(TruckyCore):
    off_text: Optional[str] = None
    on_text: Optional[str] = None
    off_color: list[int] = []
    on_color: list[int] = []
    indicator_id: Optional[str] = None
    indicator_label: Optional[str] = None
    hotkey_label: Optional[str] = None
    hotkey_default: Optional[str] = None
    hotkey_var: Optional[str] = None
    hotkey_text_var: Optional[str] = None
    show_label_title: Optional[str] = None
    show_label_subtitle: Optional[str] = None
    validated: bool = False

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True


    def on_ready(self):
        self.current_icon = self.get_icon(self.off_icon)
        self.icon_name = self.off_icon
        self.set_bottom_label(self.off_text, color=self.off_color)
        super().on_ready()

    def is_on(self, data):
        value = self.get_from_path(data)
        return value

    async def on_telemetry_update(self, event, data: dict):
        value = self.is_on(data)
        if self.last_state == value:
            return
        self.last_state = value
        if value:
            self.icon_name = self.on_icon
            if self._show_label.get_value():
                self.set_bottom_label(self.on_text, color=self.on_color)
        else:
            self.icon_name = self.off_icon
            if self._show_label.get_value():
                self.set_bottom_label(self.off_text, color=self.off_color)

        self.current_icon = self.get_icon(self.icon_name)
        self.display_icon()

    def create_event_assigners(self):
        self.event_manager.add_event_assigner(
            EventAssigner(
                id=self.indicator_id,
                ui_label=self.indicator_label,
                default_event=Input.Key.Events.DOWN,
                callback=self._toggle_action
            )
        )

    def create_generative_ui(self):
        self._indicator_hotkey = EntryRow(
            action_core=self,
            var_name=self.hotkey_var,
            default_value=self.hotkey_default,
            title=self.hotkey_label,
            complex_var_name=True,
            on_change=self._handle_hotkey,
        )

        if not self.show_label_title:
            self.show_label_title = "Show Status Label"

        if not self.show_label_subtitle:
            self.show_label_subtitle = f"Show the {self.indicator_label} status as text"

        self._show_label = SwitchRow(
            action_core=self,
            var_name=self.hotkey_text_var,
            title=self.show_label_title,
            subtitle=self.show_label_subtitle,
            default_value=True,
            on_change=self._handle_show_status,
        )

    def _update_display(self):
        if not self.icon_name:
            self.icon_name = self.off_icon
            self.current_icon = self.get_icon(self.icon_name)
        value = Icons(self.icon_name) == self.on_icon
        show_text = self._show_label.get_value()
        self.display_icon()
        if show_text:
            if value:
                self.set_bottom_label(self.on_text, color=self.on_color)
            else:
                self.set_bottom_label(self.off_text, color=self.off_color)
        else:
            self.set_bottom_label("")

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self._indicator_hotkey.widget, self._show_label.widget]

    def _toggle_action(self, _):
        self.backend.send_keystroke(self._indicator_hotkey.get_value())

    def _handle_hotkey(self, *args, **kwargs):
        self._update_display()

    def _handle_show_status(self, *args, **kwargs):
        self._update_display()