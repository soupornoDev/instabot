from pathlib import Path
from instagrapi import Client
from .logger import app_logger
from .downloader import MediaDownloader
from .utils import ensure_user_directory

class StoryDownloader:
    def __init__(self, engine: MediaDownloader) -> None:
        self.engine = engine

    def download_user_stories(self, target_username: str) -> None:
        if not self.engine.config.get("download_stories", True):
            return
        allowed, user_id = self.engine.verify_target_access(target_username)
        if not allowed:
            return
        try:
            app_logger.info(f"Retrieving transient story sequences for profile target: {target_username}")
            stories = self.engine.cl.user_stories(user_id)
            if not stories:
                app_logger.info(f"No active dynamic stories found available for user profile: {target_username}")
                return
            dest_folder = ensure_user_directory("downloads", target_username)
            for story in stories:
                shortcode = f"story_{story.id}"
                try:
                    path = self.engine.cl.story_download(story.id, folder=dest_folder)
                    self.engine.record_mgr.add_record(target_username, shortcode, "Story", "Download", "SUCCESS", str(path))
                except Exception as ex:
                    app_logger.error(f"Error capturing story tracking asset token [{shortcode}]: {ex}")
                    self.engine.record_mgr.add_record(target_username, shortcode, "Story", "Download", "FAILED", error_msg=str(ex))
        except Exception as e:
            app_logger.error(f"Failed parsing out runtime story elements: {e}")
