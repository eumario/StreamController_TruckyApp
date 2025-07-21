import os.path
import json
from loguru import logger as log

from src.backend.PluginManager.ActionHolder import ActionHolder
from src.backend.PluginManager.ActionInputSupport import ActionInputSupport
from src.backend.PluginManager.EventHolder import EventHolder
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.DeckManagement.ImageHelpers import image2pixbuf

# Actions
from .actions.speed_text import SpeedText

# Globals
from .globals import Icons
from .globals import Colors

# Gtk
from gi.repository import Gtk, Adw
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")



class Trucky(PluginBase):
    is_authroized = False
    def __init__(self):
        super().__init__(use_legacy_locale=False)
        self.init_vars()

        self.has_plugin_settings = True

        with open(os.path.join(self.PATH, "manifest.json"), "r") as f:
            manifest = json.load(f)

        backend_dir = os.path.join(self.PATH, "backend")
        backend_path = os.path.join(backend_dir, "backend.py")
        self.launch_backend(backend_path=backend_path, open_in_terminal=False, venv_path=os.path.join(self.PATH, "backend", ".venv"))
        self.wait_for_backend(5)

        # Actions
        self.register_actions(manifest)

        # Events
        self.trucky_websocket_event_holder = EventHolder(
            event_id=f"{manifest["id"]}::TelemetryUpdate",
            plugin_base=self
        )
        self.add_event_holder(self.trucky_websocket_event_holder)

        # Register Plugin
        self.register(
            plugin_name = manifest["name"],
            github_repo = manifest["github"],
            plugin_version = manifest["version"],
            app_version = manifest["app-version"]
        )

    def set_authorized(self, value: bool):
        self.is_authroized = value

    def register_actions(self, manifest):
        self.speed_text_holder = ActionHolder(
            plugin_base=self,
            action_base=SpeedText,
            action_id_suffix="SpeedText",
            action_name="Display Speed",
            action_support={
                Input.Key: ActionInputSupport.SUPPORTED,
                Input.Dial: ActionInputSupport.UNTESTED,
                Input.Touchscreen: ActionInputSupport.UNTESTED
            }
        )
        self.add_action_holder(self.speed_text_holder)

    def get_selector_icon(self) -> Gtk.Widget:
        _, rendered = self.asset_manager.icons.get_asset_values(Icons.MAIN)
        return Gtk.Image.new_from_pixbuf(image2pixbuf(rendered))

    def get_settings_area(self) -> Adw.PreferencesGroup:
        self._trucky_address = Adw.EntryRow(
            title="Trucky WebSocket Address",
        )
        self._trucky_address.set_text("ws://localhost:9977")
        pref_group = Adw.PreferencesGroup()
        pref_group.add(self._trucky_address)

        return pref_group

    def init_vars(self):
        self.add_color(Colors.NORMAL, [255,255,255,255])
        self.add_color(Colors.WARNING, [255,111,0,255])
        self.add_color(Colors.ALERT, [255,0,0,255])
        # Main Icon
        self.add_icon(Icons.MAIN, self.get_asset_path("trucky.png", ["plugin"]))

        # Categories
        self.add_icon(Icons.CAT_ALERT, self.get_asset_path("alert.png", ["categories"]))
        self.add_icon(Icons.CAT_BEACONS, self.get_asset_path("beacons.png", ["categories"]))
        self.add_icon(Icons.CAT_BUS_DOOR, self.get_asset_path("busDoorOpen.png", ["categories"]))
        self.add_icon(Icons.CAT_CAPTURE, self.get_asset_path("capture.png", ["categories"]))
        self.add_icon(Icons.CAT_CRUISE, self.get_asset_path("cruiseControl.png", ["categories"]))
        self.add_icon(Icons.CAT_DAMAGE, self.get_asset_path("damage.png", ["categories"]))
        self.add_icon(Icons.CAT_ENGINE, self.get_asset_path("engine.png", ["categories"]))
        self.add_icon(Icons.CAT_FUEL, self.get_asset_path("fuel.png", ["categories"]))
        self.add_icon(Icons.CAT_GEAR, self.get_asset_path("gear.png", ["categories"]))
        self.add_icon(Icons.CAT_HAZARD, self.get_asset_path("hazard.png", ["categories"]))
        self.add_icon(Icons.CAT_HIGH_BEAM, self.get_asset_path("highBeam.png", ["categories"]))
        self.add_icon(Icons.CAT_HORN, self.get_asset_path("horn.png", ["categories"]))
        self.add_icon(Icons.CAT_GAME_WIN, self.get_asset_path("inGameWindow.png", ["categories"]))
        self.add_icon(Icons.CAT_LEFT_TURN, self.get_asset_path("leftTurn.png", ["categories"]))
        self.add_icon(Icons.CAT_LIGHTS, self.get_asset_path("lights.png", ["categories"]))
        self.add_icon(Icons.CAT_LOW_BEAM, self.get_asset_path("lowBeams.png", ["categories"]))
        self.add_icon(Icons.CAT_MOTOR_BRAKE, self.get_asset_path("motorBrake.png", ["categories"]))
        self.add_icon(Icons.CAT_NAVIGATION, self.get_asset_path("navigation.png", ["categories"]))
        self.add_icon(Icons.CAT_NEXT_PREV_RADIO, self.get_asset_path("nextPrevRadio.png", ["categories"]))
        self.add_icon(Icons.CAT_NEXT_RADIO, self.get_asset_path("nextRadio.png", ["categories"]))
        self.add_icon(Icons.CAT_ODOMETER, self.get_asset_path("odometer.png", ["categories"]))
        self.add_icon(Icons.CAT_PARKING_BRAKE, self.get_asset_path("parkingBrake.png", ["categories"]))
        self.add_icon(Icons.CAT_PARKING_LIGHTS, self.get_asset_path("parkingLightso.png", ["categories"]))
        self.add_icon(Icons.CAT_PLAY, self.get_asset_path("play.png", ["categories"]))
        self.add_icon(Icons.CAT_RADIO, self.get_asset_path("radio.png", ["categories"]))
        self.add_icon(Icons.CAT_RECORDING, self.get_asset_path("recording.png", ["categories"]))
        self.add_icon(Icons.CAT_RETARDER, self.get_asset_path("retarder.png", ["categories"]))
        self.add_icon(Icons.CAT_RIGHT_TURN, self.get_asset_path("rightTurn.png", ["categories"]))
        self.add_icon(Icons.CAT_RPM, self.get_asset_path("rpm.png", ["categories"]))
        self.add_icon(Icons.CAT_SCREENSHOT, self.get_asset_path("screenshot.png", ["categories"]))
        self.add_icon(Icons.CAT_SPEED_LIMIT, self.get_asset_path("speedLimit.png", ["categories"]))
        self.add_icon(Icons.CAT_SPEEDOMETER, self.get_asset_path("speedometer.png", ["categories"]))
        self.add_icon(Icons.CAT_TRAILER, self.get_asset_path("trailer.png", ["categories"]))
        self.add_icon(Icons.CAT_TURN_INDICATORS, self.get_asset_path("turnIndicators.png", ["categories"]))
        self.add_icon(Icons.CAT_VOLUME, self.get_asset_path("volume.png", ["categories"]))
        self.add_icon(Icons.CAT_VOLUME_DOWN, self.get_asset_path("volumeDown.png", ["categories"]))
        self.add_icon(Icons.CAT_VOLUME_UP, self.get_asset_path("volumeUp.png", ["categories"]))
        self.add_icon(Icons.CAT_WIPERS, self.get_asset_path("wipers.png", ["categories"]))

        # Actions
        self.add_icon(Icons.ACT_ACCIDENT, self.get_asset_path("accident_button.png", ["actions"]))
        self.add_icon(Icons.ACT_ATS, self.get_asset_path("ats.png", ["actions"]))
        self.add_icon(Icons.ACT_ATS_SPEED_LIMIT, self.get_asset_path("atsSpeedLimit.png", ["actions"]))
        self.add_icon(Icons.ACT_ATS_TRUCK, self.get_asset_path("atsTruck.png", ["actions"]))
        self.add_icon(Icons.ACT_BEACON, self.get_asset_path("beacon.png", ["actions"]))
        self.add_icon(Icons.ACT_BEACON_OFF, self.get_asset_path("beaconsOff.png", ["actions"]))
        self.add_icon(Icons.ACT_BEACON_ON, self.get_asset_path("beaconsOn.png", ["actions"]))
        self.add_icon(Icons.ACT_BUS_DOOR_OPEN, self.get_asset_path("busDoorOpen.png", ["actions"]))
        self.add_icon(Icons.ACT_CAPTURE, self.get_asset_path("capture.png", ["actions"]))
        self.add_icon(Icons.ACT_CARGO_DAMAGE, self.get_asset_path("cargoDamage.png", ["actions"]))
        self.add_icon(Icons.ACT_CRUISE_CONTROL_OFF, self.get_asset_path("cruiseControlOff.png", ["actions"]))
        self.add_icon(Icons.ACT_CRUISE_CONTROL_ON, self.get_asset_path("cruiseControlOn.png", ["actions"]))
        self.add_icon(Icons.ACT_ENGINE_START, self.get_asset_path("engineStart.png", ["actions"]))
        self.add_icon(Icons.ACT_ENGINE_STOP, self.get_asset_path("engineStop.png", ["actions"]))
        self.add_icon(Icons.ACT_ETS2, self.get_asset_path("ets2.png", ["actions"]))
        self.add_icon(Icons.ACT_ETS2_SPEED_LIMIT, self.get_asset_path("ets2speedLimit.png", ["actions"]))
        self.add_icon(Icons.ACT_ETS2_TRUCK, self.get_asset_path("ets2Truck.png", ["actions"]))
        self.add_icon(Icons.ACT_FUEL, self.get_asset_path("fuel.png", ["actions"]))
        self.add_icon(Icons.ACT_GEAR, self.get_asset_path("gear.png", ["actions"]))
        self.add_icon(Icons.ACT_HAZARD_OFF, self.get_asset_path("hazardOff.png", ["actions"]))
        self.add_icon(Icons.ACT_HAZARD_ON, self.get_asset_path("hazardOn.png", ["actions"]))
        self.add_icon(Icons.ACT_HIGH_BEAM_OFF, self.get_asset_path("highBeamOff.png", ["actions"]))
        self.add_icon(Icons.ACT_HIGH_BEAM_ON, self.get_asset_path("highBeamOn.png", ["actions"]))
        self.add_icon(Icons.ACT_HORN, self.get_asset_path("horn.png", ["actions"]))
        self.add_icon(Icons.ACT_GAME_WIN, self.get_asset_path("inGameWindow.png", ["actions"]))
        self.add_icon(Icons.ACT_LEFT_TURN_OFF, self.get_asset_path("leftTurnOff.png", ["actions"]))
        self.add_icon(Icons.ACT_LEFT_TURN_ON, self.get_asset_path("leftTurnOn.png", ["actions"]))
        self.add_icon(Icons.ACT_LIGHTS_OFF, self.get_asset_path("lightsOff.png", ["actions"]))
        self.add_icon(Icons.ACT_LIGHTS_ON, self.get_asset_path("lightsOn.png", ["actions"]))
        self.add_icon(Icons.ACT_LOW_BEAMS_OFF, self.get_asset_path("lowBeamsOff.png", ["actions"]))
        self.add_icon(Icons.ACT_LOW_BEAMS_ON, self.get_asset_path("lowBeamsOn.png", ["actions"]))
        self.add_icon(Icons.ACT_MOTOR_BRAKE_OFF, self.get_asset_path("motorBrakeOff.png", ["actions"]))
        self.add_icon(Icons.ACT_MOTOR_BRAKE_ON, self.get_asset_path("motorBrakeOn.png", ["actions"]))
        self.add_icon(Icons.ACT_NAVIGATION, self.get_asset_path("navigation.png", ["actions"]))
        self.add_icon(Icons.ACT_NEXT_RADIO, self.get_asset_path("nextRadio.png", ["actions"]))
        self.add_icon(Icons.ACT_ODOMETER, self.get_asset_path("odometer.png", ["actions"]))
        self.add_icon(Icons.ACT_PARKING_BRAKE_OFF, self.get_asset_path("parkingBrakeOff.png", ["actions"]))
        self.add_icon(Icons.ACT_PARKING_BRAKE_ON, self.get_asset_path("parkingBrakeOn.png", ["actions"]))
        self.add_icon(Icons.ACT_PARKING_LIGHTS_OFF, self.get_asset_path("parkingLightsOff.png", ["actions"]))
        self.add_icon(Icons.ACT_PARKING_LIGHTS_ON, self.get_asset_path("parkingLightsOn.png", ["actions"]))
        self.add_icon(Icons.ACT_POLICE_BUTTON, self.get_asset_path("police_button.png", ["actions"]))
        self.add_icon(Icons.ACT_PREV_RADIO, self.get_asset_path("prevRadio.png", ["actions"]))
        self.add_icon(Icons.ACT_RADIO, self.get_asset_path("radio.png", ["actions"]))
        self.add_icon(Icons.ACT_RADIO_ON, self.get_asset_path("radioOn.png", ["actions"]))
        self.add_icon(Icons.ACT_RETARDER_OFF, self.get_asset_path("retarderOff.png", ["actions"]))
        self.add_icon(Icons.ACT_RETARDER_ON, self.get_asset_path("retarderOn.png", ["actions"]))
        self.add_icon(Icons.ACT_RIGHT_TURN_OFF, self.get_asset_path("rightTurnOff.png", ["actions"]))
        self.add_icon(Icons.ACT_RIGHT_TURN_ON, self.get_asset_path("rightTurnOn.png", ["actions"]))
        self.add_icon(Icons.ACT_ROADSIDE_HAZARD, self.get_asset_path("roadside_hazard_button.png", ["actions"]))
        self.add_icon(Icons.ACT_ROADWORKS, self.get_asset_path("roadworks_button.png", ["actions"]))
        self.add_icon(Icons.ACT_RPM, self.get_asset_path("rpm.png", ["actions"]))
        self.add_icon(Icons.ACT_SCREENSHOT, self.get_asset_path("screenshot.png", ["actions"]))
        self.add_icon(Icons.ACT_SPEED3, self.get_asset_path("speed3.png", ["actions"]))
        self.add_icon(Icons.ACT_SPEEDOMETER, self.get_asset_path("speedometer.png", ["actions"]))
        self.add_icon(Icons.ACT_START_RECORDING, self.get_asset_path("startRecording.png", ["actions"]))
        self.add_icon(Icons.ACT_TMP, self.get_asset_path("tmp.png", ["actions"]))
        self.add_icon(Icons.ACT_TRAFFIC_MODERATE, self.get_asset_path("traffic_moderate_button.png", ["actions"]))
        self.add_icon(Icons.ACT_TRAFFIC_QUEUE, self.get_asset_path("traffic_queue_button.png", ["actions"]))
        self.add_icon(Icons.ACT_TRAILER_DAMAGE, self.get_asset_path("trailerDamage.png", ["actions"]))
        self.add_icon(Icons.ACT_TRAILER_OFF, self.get_asset_path("trailerOff.png", ["actions"]))
        self.add_icon(Icons.ACT_TRAILER_ON, self.get_asset_path("trailerOn.png", ["actions"]))
        self.add_icon(Icons.ACT_VOLUME, self.get_asset_path("volume.png", ["actions"]))
        self.add_icon(Icons.ACT_VOLUME_DOWN, self.get_asset_path("volumeDown.png", ["actions"]))
        self.add_icon(Icons.ACT_VOLUME_UP, self.get_asset_path("volumeUp.png", ["actions"]))
        self.add_icon(Icons.ACT_WIPERS_OFF, self.get_asset_path("wipersOff.png", ["actions"]))
        self.add_icon(Icons.ACT_WIPERS_ON, self.get_asset_path("wipersOn.png", ["actions"]))

        for icon in Icons:
            asset = self.asset_manager.icons.get_asset(icon).to_json()
            if not os.path.exists(asset['path']):
                log.error(f"Failed to find icon {icon} for {asset['path']}")