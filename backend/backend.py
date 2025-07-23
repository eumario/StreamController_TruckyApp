import json
import time
from loguru import logger as log
from typing import Dict, Any

from streamcontroller_plugin_tools import BackendBase
from trucky_websocket import TruckyWebsocket


class TruckyAppBackend(BackendBase):
    welcome_packet: dict[str,str] = {
        "action": "hello",
        "app": "streamdeck"
    }
    uri: str = "ws://localhost:9977/dashboard"
    reconnect_delay: float = 5.0
    max_retries: int = 30
    running: bool = True
    settings_changed: bool = False
    authorized: bool = False
    stopping: bool = False
    prev_telemetry: float = 0

    def __init__(self) -> None:
        super().__init__()
        self.client = TruckyWebsocket(
            url=self.uri,
            reconnect_delay=self.reconnect_delay,
            max_reconnect_attempts=self.max_retries,
            on_message=self.message_handler,
            on_open=self.connected_handler,
            on_close=self.closed_handler
        )

        self.thread = self.client.start_async()
        self.main_loop()

    def main_loop(self):
        while True:
            time.sleep(0.01)

            if self.settings_changed:
                self.client.stop()
                if self.thread.is_alive:
                    self.thread.join()
                self.client.url = self.uri
                self.thread = self.client.start_async()
                continue

            if self.running:
                continue

            if self.stopping:
                break

            self.client.stop()
            self.stopping = True
            if self.thread.is_alive():
                self.thread.join()
                break

    ## Handle RpyC disconnect
    def on_disconnect(self, conn):
        self.running = False
        super().on_disconnect(conn)

    ## WebSocketApp Handlers
    def connected_handler(self) -> None:
        self.send_to_trucky(self.welcome_packet)

    def closed_handler(self, ws, status_code, message) -> None:
        pass

    def message_handler(self, message) -> None:
        try:
            data = json.loads(message)

            if isinstance(data, dict) and 'type' in data:
                if data['type'] == "authorization":
                    self.frontend.set_authorized(data['data']['permission'])
                    log.info("Connected to Trucky!")
                elif data['type'] == "telemetry":
                    stamp = time.time()
                    if stamp - self.prev_telemetry > 0.1:
                        self.prev_telemetry = stamp
                        self.frontend.trucky_websocket_event_holder.trigger_event(data['data'])
        except json.JSONDecodeError:
            print(f"Received unknown packet: {message}")

    ## Trucky API
    def send_to_trucky(self, message: Dict[str, Any]) -> bool:
        data = json.dumps(message)
        return self.client.send(data)

    def send_keystroke(self, key: str):
        if len(key) > 1:
            if key == "SPACE":
                key = " "
        return self.send_to_trucky({
            "action": "sendKeystroke",
            "hotkeys": key
        })

    def send_window(self, window: str):
        return self.send_to_trucky({
            "action": "window",
            "window": window
        })

    def get_current_radio(self):
        return self.send_to_trucky({
            "action": "feature",
            "feature": "current-radio"
        })

    def play_radio(self):
        return self.send_to_trucky({
            "action": "feature",
            "feature": "play-radio"
        })

    def send_report(self, report_type: str):
        return self.send_to_trucky({
            "action": "report",
            "reportType": report_type
        })

    def send_command(self, command: str):
        return self.send_to_trucky({
            "action": "feature",
            "feature": command
        })

    def take_screenshot(self):
        return self.send_to_trucky({
            "action": "feature",
            "feature": "screenshot"
        })

    def open_bus_door(self):
        return self.send_to_trucky({
            "action": "feature",
            "feature": "open-bus-door"
        })

    def start_game(self, game: str):
        return self.send_to_trucky({
            "action": "startGame",
            "game": game
        })

    def record_replay(self):
        return self.send_to_trucky({
            "action": "feature",
            "feature": "record-replay"
        })

    def toggle_recording(self):
        return self.send_to_trucky({
            "action": "feature",
            "feature": "toggle-recording"
        })

backend = TruckyAppBackend()