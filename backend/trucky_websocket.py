import websocket
import time
import threading
from loguru import logger as log
from typing import Optional, Callable

class TruckyWebsocket:
    def __init__(
            self,
            url: str,
            reconnect_delay: float = 5.0,
            max_reconnect_attempts: Optional[int] = None,
            on_message: Optional[Callable] = None,
            on_error: Optional[Callable] = None,
            on_open: Optional[Callable] = None,
            on_close: Optional[Callable] = None
    ):
        self.url = url
        self.reconnect_delay = reconnect_delay
        self.max_reconnect_attempts = max_reconnect_attempts
        self.reconnect_count = 0
        self.should_reconnect = True
        self.ws = None
        self.lock = threading.Lock()
        self.debug = False

        self.user_on_message = on_message
        self.user_on_error = on_error
        self.user_on_open = on_open
        self.user_on_close = on_close

    def _on_message(self, ws, message):
        if self.debug:
            log.info(f"Received message: {message[:100]}...")
        if self.user_on_message:
            self.user_on_message(message)

    def _on_error(self, ws, error):
        log.error(f"WebSocket error: {error}")
        if self.user_on_error:
            self.user_on_error(error)

    def _on_open(self, ws):
        log.info("Websocket Connection opened")
        self.reconnect_count = 0
        if self.user_on_open:
            self.user_on_open()

    def _on_close(self, ws, close_status_code, close_msg):
        log.info(f"Websocket connection closed: {close_status_code} - {close_msg}")
        if self.user_on_close:
            self.user_on_close(ws, close_status_code, close_msg)

        if self.should_reconnect:
            self._reconnect()

    def _reconnect(self):
        if self.max_reconnect_attempts and self.reconnect_count >= self.max_reconnect_attempts:
            log.error(f"Max reconnect attempts ({self.max_reconnect_attempts}) reached. Giving Up.")
            return

        self.reconnect_count += 1
        log.info(f"Reconnecting in {self.reconnect_delay} seconds... (attempt {self.reconnect_count})")

        time.sleep(self.reconnect_delay)

        if self.should_reconnect:
            log.info(f"Attempting to reconnect (attempt {self.reconnect_count})")
            self._create_connection()

    def _create_connection(self):
        try:
            with self.lock:
                if self.ws:
                    self.ws.close()

                self.ws = websocket.WebSocketApp(
                    self.url,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_open=self._on_open,
                    on_close=self._on_close
                )

            self.ws.run_forever()
        except Exception as e:
            log.error(f"Failed to create WebSocket connection: {e}")
            if self.should_reconnect:
                self._reconnect()

    def start(self):
        log.info(f"Starting WebSocket connection to {self.url}")
        self.should_reconnect = True
        self.reconnect_count = 0
        self._create_connection()

    def start_async(self):
        thread = threading.Thread(target=self.start, daemon=True)
        thread.start()
        return thread

    def send(self, data):
        with self.lock:
            if self.ws and self.ws.sock and self.ws.sock.connected:
                try:
                    self.ws.send(data)
                    if self.debug:
                        log.info(f"Sent message: {data[:100]}...")
                except Exception as e:
                    log.error(f"Failed to send message: {e}")
            else:
                log.warning("WebSocket not connected. Cannot send message.")

    def stop(self):
        log.info("Stopping WebSocket connection")
        self.should_reconnect = False
        with self.lock:
            if self.ws:
                self.ws.close()