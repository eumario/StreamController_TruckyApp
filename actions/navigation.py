from enum import Enum
from GtkHelper.ComboRow import SimpleComboRowItem
from GtkHelper.GenerativeUI.ComboRow import ComboRow
from .trucky_indicator_display import TruckyIndicatorDisplay
from ..globals import Icons
from src.backend.PluginManager.EventAssigner import EventAssigner
from src.backend.PluginManager.InputBases import Input
from gi.repository import Adw
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class NavigationOptions(Enum):
    DISTANCE = SimpleComboRowItem("distance", "Distance")
    DURATION = SimpleComboRowItem("duration", "Estimated Time Left")
    ARRIVAL_TIME = SimpleComboRowItem("arrivalTime", "Estimated Arrival Time")

class Navigation(TruckyIndicatorDisplay):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_path = ["navigation", "distance_converted"]
        self.units = ["units", "distance"]
        self.icon_keys = [Icons.ACT_NAVIGATION]
        self.icon_name = Icons.ACT_NAVIGATION
        self.current_icon = self.get_icon(Icons.ACT_NAVIGATION)
        self.text_color = [255, 255, 255, 255]

    def create_generative_ui(self):
        self._naviation_options = ComboRow(
            action_core=self,
            var_name="navigation.mode",
            default_value=NavigationOptions.DISTANCE.value,
            title="Navigation Display",
            subtitle="Mode in which to show for navigation",
            complex_var_name=True,
            items=[
                NavigationOptions.DISTANCE.value,
                NavigationOptions.ARRIVAL_TIME.value,
                NavigationOptions.DURATION.value
            ],
            on_change=self._handle_navigation_display_mode
        )

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self._naviation_options.widget]

    def create_event_assigners(self):
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="switch-nav-display-mode",
                ui_label="Switch Nav Mode",
                default_event=Input.Key.Events.DOWN,
                callback=self._switch_display_mode
            )
        )

    def on_telemetry_update(self, event, data: dict):
        if data["navigation"] is not None:
            check = self.get_from_path(data)
            units = self.get_from_specific_path(self.units, data)
        else:
            check = None
            units = ""

        if self.state == check:
            return

        self.last_state = check

        if check is None:
            self.display_text("No Info", "top")
            return

        if self.data_path[1] == "distance_converted":
            self.display_text(f"{check} {units}", "top")
        elif type(check) == int:
            self.display_text(f"{check}", "top")
        else:
            self.display_text(check.replace(" ",""), "top")

    def _switch_display_mode(self, _):
        item = self._naviation_options.get_selected_item()
        if item.get_value() == "distance":
            self._naviation_options.set_selected_item(NavigationOptions.DURATION.value)
        elif item.get_value() == "duration":
            self._naviation_options.set_selected_item(NavigationOptions.ARRIVAL_TIME.value)
        else:
            self._naviation_options.set_selected_item(NavigationOptions.DISTANCE.value)

    def _handle_navigation_display_mode(self, _, new: SimpleComboRowItem, __):
        id = new.get_value()
        if id == "distance":
            self.data_path[1] = "distance_converted"
        elif id == "duration":
            self.data_path[1] = "estimated_real_life_time_duration"
        else:
            self.data_path[1] = "real_life_arrival_time_formatted"
        self.last_state = ""