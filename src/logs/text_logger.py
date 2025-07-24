from datetime import datetime
from src.logs.listener import Listener


class TextLogger(Listener):
    def __init__(self, file_name: str = "log.txt"):
        self.file_name = file_name

    def update(self, payload):
        log_entry = self._format_entry(payload)
        with open(self.file_name, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry + "\n")

    def _format_entry(self, payload) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_info = f"[{timestamp}] EVENT: {payload.get('event_type', 'UNKNOWN')}\n"
        details = "\n".join(
            f"  {k}: {v}" for k, v in payload.items() if k != "event_type"
        )
        return event_info + details
