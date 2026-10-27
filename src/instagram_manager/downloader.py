from instagrapi import Client
from .logger import app_logger
from .records import RecordManager
from .config import ConfigManager

class MediaDownloader:
    def __init__(self, client: Client, config: ConfigManager, record_mgr: RecordManager) -> None:
        self.cl = client
        self.config = config
        self.record_mgr = record_mgr

    def verify_target_access(self, target_username: str) -> tuple[bool, str]:
        try:
            user_id = self.cl.user_id_from_username(target_username)
            info = self.cl.user_info(user_id)
            if info.is_private and not info.following_tag:
                app_logger.warning(f"Target account '{target_username}' is private and you do not follow them.")
                return False, ""
            return True, user_id
        except Exception as e:
            app_logger.error(f"Unable to safely resolve tracking target parameters for '{target_username}': {e}")
            return False, ""
