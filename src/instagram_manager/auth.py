import getpass
from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    TwoFactorRequired,
    LoginRequired,
    ChallengeRequired
)
from .logger import app_logger

class AuthenticationManager:
    def __init__(self, client: Client, session_dir: str = "sessions") -> None:
        self.cl = client
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.current_username = ""

    def get_session_path(self, username: str) -> Path:
        return self.session_dir / f"{username}_settings.json"

    def load_session(self, username: str) -> bool:
        session_path = self.get_session_path(username)
        if not session_path.exists():
            return False
        try:
            self.cl.load_settings(session_path)
            app_logger.info(f"Loaded existing session settings for user: {username}")
            self.current_username = username
            return True
        except Exception as e:
            app_logger.warning(f"Failed to load settings file for {username}: {e}")
            return False

    def validate_session(self) -> bool:
        try:
            if not self.current_username:
                return False
            self.cl.get_timeline_feed()
            app_logger.info("Session token verification validated successfully.")
            return True
        except LoginRequired:
            app_logger.warning("Active execution layer reports expired session signature tokens.")
            return False
        except Exception as e:
            app_logger.error(f"Error checking verification endpoint state: {e}")
            return False

    def login(self, username: str) -> bool:
        self.current_username = username
        session_path = self.get_session_path(username)
        if self.load_session(username):
            if self.validate_session():
                return True
        
        password = getpass.getpass(prompt=f"Enter Password for Instagram Account [{username}]: ")
        try:
            app_logger.info(f"Attempting login command sequence for profile: {username}")
            self.cl.login(username, password)
            self.cl.dump_settings(session_path)
            app_logger.info("Login successful. Authorization configuration persisted cleanly.")
            return True
        except TwoFactorRequired:
            app_logger.warning("Two-Factor Authentication is required for this account.")
            verification_code = input("Enter the 2FA verification code sent to your device: ").strip()
            try:
                self.cl.login(username, password, verification_code=verification_code)
                self.cl.dump_settings(session_path)
                app_logger.info("2FA Challenge validated successfully. Session persisted.")
                return True
            except Exception as e2fa:
                app_logger.error(f"2FA verification failed: {e2fa}")
                return False
        except BadPassword:
            app_logger.error("Authentication rejected: Invalid password provided.")
            return False
        except ChallengeRequired:
            app_logger.error("Instagram has issued a security checkpoint challenge. Please resolve it via a web browser or official app.")
            return False
        except Exception as e:
            app_logger.error(f"Unexpected error encountered during login pipeline processing: {e}")
            return False
