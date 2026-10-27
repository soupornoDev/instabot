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
            medias = self.engine.cl.user_medias(user_id, amount=limit)
            dest_folder = ensure_user_directory("downloads", target_username)
            for media in medias:
                self._process_media(media, target_username, dest_folder)
        except Exception as e:
            app_logger.error(f"Failed parsing post streams: {e}")

    def _process_media(self, media: Media, username: str, dest: Path) -> None:
        shortcode = media.code
        try:
            if media.media_type == 1:
                path = self.engine.cl.photo_download(media.pk, folder=dest)
                self.engine.record_mgr.add_record(username, shortcode, "Photo", "Download", "SUCCESS", str(path))
            elif media.media_type == 2:
                if self.engine.config.get("download_videos", True):
                    path = self.engine.cl.video_download(media.pk, folder=dest)
                    self.engine.record_mgr.add_record(username, shortcode, "Video", "Download", "SUCCESS", str(path))
            elif media.media_type == 8:
                paths = self.engine.cl.album_download(media.pk, folder=dest)
                self.engine.record_mgr.add_record(username, shortcode, "Carousel", "Download", "SUCCESS", str(paths))
            app_logger.info(f"Successfully processed post entity [{shortcode}]")
        except Exception as e:
            app_logger.error(f"Error handling post asset item reference [{shortcode}]: {e}")
            self.engine.record_mgr.add_record(username, shortcode, "Post", "Download", "FAILED", error_msg=str(e))
