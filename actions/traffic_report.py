from enum import StrEnum, Enum
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

from GtkHelper.ComboRow import SimpleComboRowItem
from GtkHelper.GenerativeUI.ComboRow import ComboRow
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

class TrafficReportOptions(Enum):
    ACCIDENT = SimpleComboRowItem("accident", "Accident")
    TRAFFIC_QUEUE = SimpleComboRowItem("traffic-queue", "Traffic Queue")
    TRAFFIC_MODERATE = SimpleComboRowItem("traffic-moderate", "Traffic Moderate")
    POLICE = SimpleComboRowItem("police", "Police Spotted")
    ROADSIZE_HAZARD = SimpleComboRowItem("roadsize-hazard", "Roadside Hazard")
    ROADWORKS = SimpleComboRowItem("roadworks", "Roadworks")

class TrafficReport(TruckyCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_configuration = True
        self.icon_keys = [Icons.ACT_ACCIDENT, Icons.ACT_TRAFFIC_QUEUE, Icons.ACT_TRAFFIC_MODERATE,
                          Icons.ACT_POLICE_BUTTON, Icons.ACT_ROADSIDE_HAZARD, Icons.ACT_ROADWORKS]

        self.current_icon = self.get_icon(Icons.ACT_ACCIDENT)
        self.icon_name = Icons.ACT_ACCIDENT

    def create_event_assigners(self):
        self.event_manager.add_event_assigner(
            EventAssigner(
                id="traffic-report",
                ui_label="Traffic Report",
                default_event=Input.Key.Events.DOWN,
                callback=self._make_report,
            )
        )

    def create_generative_ui(self):
        self._report_type = ComboRow(
            action_core=self,
            var_name="traffic.report",
            default_value=TrafficReportOptions.ACCIDENT.value,
            title="Traffic Report",
            subtitle="Select a Report to Make",
            complex_var_name=True,
            items=[
                TrafficReportOptions.ACCIDENT.value,
                TrafficReportOptions.TRAFFIC_QUEUE.value,
                TrafficReportOptions.TRAFFIC_MODERATE.value,
                TrafficReportOptions.POLICE.value,
                TrafficReportOptions.ROADSIZE_HAZARD.value,
                TrafficReportOptions.ROADWORKS.value,
            ],
            on_change=self._handle_report_change,
        )

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        return [self._report_type.widget]

    def _make_report(self, _):
        self.backend.send_report(self._report_type.get_value())

    def _handle_report_change(self, _, new: SimpleComboRowItem, __):
        self.icon_name = Icons(new)
        self.current_icon = self.get_icon(self.icon_name)
        self.display_icon()