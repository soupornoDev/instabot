from pathlib import Path
from .logger import app_logger
from .downloader import MediaDownloader
from .utils import ensure_user_directory

class ReelDownloader:
    def __init__(self, engine: MediaDownloader) -> None:
        self.engine = engine

    def download_user_reels(self, target_username: str, limit: int = 5) -> None:
        if not self.engine.config.get("download_reels", True):
            app_logger.info("Dynamic processing configurations flag Reels handling processes down.")
            return
        allowed, user_id = self.engine.verify_target_access(target_username)
        if not allowed:
            return
        try:
            app_logger.info(f"Querying short clip tracks for target identification: {target_username}")
            medias = self.engine.cl.user_medias(user_id, amount=limit * 2)
            reels = [m for m in medias if m.product_type == "clips"]
            dest_folder = ensure_user_directory("downloads", target_username)
            processed_count = 0
            for reel in reels:
                if processed_count >= limit:
                    break
                shortcode = reel.code
                try:
                    path = self.engine.cl.video_download(reel.pk, folder=dest_folder)
                    self.engine.record_mgr.add_record(target_username, shortcode, "Reel", "Download", "SUCCESS", str(path))
                    app_logger.info(f"Successfully preserved Reel asset element: {shortcode}")
                    processed_count += 1
                except Exception as ex:
                    app_logger.error(f"Error transferring Reel tracking token [{shortcode}]: {ex}")
                    self.engine.record_mgr.add_record(target_username, shortcode, "Reel", "Download", "FAILED", error_msg=str(ex))
        except Exception as e:
            app_logger.error(f"Failed executing Reels collection routines: {e}")
