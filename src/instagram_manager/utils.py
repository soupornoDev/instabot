import re
from pathlib import Path

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)

def ensure_user_directory(base_dir: str, username: str) -> Path:
    target_path = Path(base_dir) / sanitize_filename(username)
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path
