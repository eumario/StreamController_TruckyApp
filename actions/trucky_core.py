from typing import Optional

from ..globals import Icons
from src.backend.PluginManager.ActionCore import ActionCore
from src.backend.PluginManager.PluginSettings.Asset import Color, Icon


class TruckyCore(ActionCore):
    last_state: any = None
    data_path: list[str] = []
    off_icon: Optional[Icons] = None
    on_icon: Optional[Icons] = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup AssetManager values
        self.icon_keys = []
        self.color_keys = []
        self.current_icon: Icon = None
        self.current_color: Color = None
        self.icon_name = ""
        self.color_name = ""
        self.backend: 'Backend' = self.plugin_base.backend

        self.plugin_base.connect_to_event(event_id="dev_eumario_TruckyApp::TelemetryUpdate",
                                          callback=self.on_telemetry_update)

        self.plugin_base.asset_manager.icons.add_listener(self._icon_changed)
        self.plugin_base.asset_manager.colors.add_listener(self._color_changed)

        # Setup action related stuff
        self.create_generative_ui()
        self.create_event_assigners()

    def on_ready(self):
        super().on_ready()
        self.display_icon()
        self.display_color()

    def get_from_path(self, data):
        value = data
        for i in self.data_path:
            if i in value:
                value = value[i]
            else:
                return None
        return value

    def get_from_specific_path(self, path: list[str], data):
        value = data
        for i in path:
            if i in value:
                value = value[i]
            else:
                return None
        return value

    def create_generative_ui(self):
        pass

    def create_event_assigners(self):
        pass

    async def on_telemetry_update(self, event, data: dict):
        pass

    def display_icon(self):
        if not self.current_icon:
            return
        _, rendered = self.current_icon.get_values()
        if rendered:
            self.set_media(image=rendered)

    async def _icon_changed(self, event: str, key: str, asset):
        if not key in self.icon_keys:
            return

        if key != self.icon_name:
            return
        self.current_icon = asset
        self.icon_name = key
        self.display_icon()

    def display_color(self):
        if not self.current_color:
            return
        color = self.current_color.get_values()
        try:
            self.set_background_color(color)
        except:
            # Sometimes we try to call this too early, and it leads to
            # console errors, but no real errors. Ignoring this for now
            pass

    async def _color_changed(self, event: str, key: str, asset):
        if not key in self.color_keys:
            return
        if key != self.color_name:
            return
        self.current_color = asset
        self.color_name = key
        self.display_color()