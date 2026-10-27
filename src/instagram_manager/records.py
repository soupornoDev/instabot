import datetime
from pathlib import Path

class RecordManager:
    def __init__(self, record_path: str = "download_record.txt") -> None:
        self.record_path = Path(record_path)

    def add_record(self, username: str, media_id: str, media_type: str, 
                   operation: str, status: str, path: str = "N/A", 
                   error_msg: str = "") -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record_entry = (
            f"[{timestamp}]\n"
            f"Username: {username}\n"
            f"Media: {media_id}\n"
            f"Type: {media_type}\n"
            f"Operation: {operation}\n"
            f"Status: {status}\n"
            f"Path: {path}\n"
        )
        if error_msg:
            record_entry += f"Error: {error_msg}\n"
        record_entry += "\n"
        
        try:
            with open(self.record_path, "a", encoding="utf-8") as f:
                f.write(record_entry)
        except IOError as e:
            from .logger import app_logger
            app_logger.error(f"Failed writing execution transaction out to ledger: {e}")
