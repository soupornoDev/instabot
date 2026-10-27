import json
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    def __init__(self, config_path: str = "config.json") -> None:
        self.config_path = Path(config_path)
        self.data: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if not self.config_path.exists():
            self.data = {
                "target_username": "sarmistha8939",
                "download_posts": True,
                "download_reels": True,
                "download_stories": True,
                "save_metadata": True,
                "download_videos": True,
                "download_thumbnails": False,
                "comment_template": "Owo beautiful picture 💝💝 message sent from @{username}"
            }
            self.save()
        else:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def save(self) -> None:
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()
