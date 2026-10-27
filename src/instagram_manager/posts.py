from pathlib import Path
from instagrapi.types import Media
from .logger import app_logger
from .downloader import MediaDownloader
from .utils import ensure_user_directory

class PostDownloader:
    def __init__(self, engine: MediaDownloader) -> None:
        self.engine = engine

    def download_user_posts(self, target_username: str, limit: int = 5) -> None:
        allowed, user_id = self.engine.verify_target_access(target_username)
        if not allowed:
            return
        try:
            app_logger.info(f"Querying post archives for profile identifier: {target_username}")
            
            # ফিক্সড লজিক: limit যদি ০ (স্টার থেকে রূপান্তরিত) হয়, তবে এটি প্রোফাইলের সব পোস্ট নামিয়ে আনবে।
            medias = self.engine.cl.user_medias(user_id, amount=limit)
            
            dest_folder = ensure_user_directory("downloads", target_username)
            for media in medias:
                self._process_media(media, target_username, dest_folder)
        except Exception as e:
            app_logger.error(f"Failed parsing post streams: {e}")
