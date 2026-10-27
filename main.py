#!/usr/bin/env python3
import sys
from pathlib import Path
from instagrapi import Client

from src.instagram_manager.config import ConfigManager
from src.instagram_manager.logger import app_logger
from src.instagram_manager.records import RecordManager
from src.instagram_manager.auth import AuthenticationManager
from src.instagram_manager.downloader import MediaDownloader
from src.instagram_manager.posts import PostDownloader
from src.instagram_manager.reels import ReelDownloader
from src.instagram_manager.stories import StoryDownloader

def print_menu() -> None:
    print("\n" + "="*40)
    print("       INSTAGRAM MEDIA MANAGER")
    print("="*40)
    print("1. Login to Instagram")
    print("2. Validate Saved Session")
    print("3. Download Posts")
    print("4. Download Reels")
    print("5. Download Accessible Stories")
    print("6. Preview Comment Text")
    print("7. View Download Records")
    print("8. View Application Logs")
    print("9. Exit")
    print("="*40)

def main() -> None:
    Path("downloads").mkdir(exist_ok=True)
    Path("sessions").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    config = ConfigManager()
    record_mgr = RecordManager()
    
    cl = Client()
    auth_mgr = AuthenticationManager(cl)
    engine = MediaDownloader(cl, config, record_mgr)
    
    post_dl = PostDownloader(engine)
    reel_dl = ReelDownloader(engine)
    story_dl = StoryDownloader(engine)
    
    my_username = "__dark.tirtha__"
    auth_mgr.load_session(my_username)
    
    while True:
        print_menu()
        choice = input("Select an option (1-9): ").strip()
        
        if choice == "1":
            success = auth_mgr.login(my_username)
            if success:
                print(f"[+] Successfully authenticated as {my_username}")
            else:
                print("[-] Authentication flow processing failed. Review system logs.")
        elif choice == "2":
            if auth_mgr.validate_session():
                print("[+] Active session configurations validated successfully.")
            else:
                print("[-] Active session invalid or expired. Please re-authenticate (Option 1).")
        elif choice == "3":
            target = config.get("target_username", "sarmistha8939")
            limit = input("Enter max number of posts to fetch [Default: 5]: ").strip()
            limit_val = int(limit) if limit.isdigit() else 5
            print(f"[*] Processing posts query matching profile trace target: {target}")
            post_dl.download_user_posts(target, limit=limit_val)
        elif choice == "4":
            target = config.get("target_username", "sarmistha8939")
            limit = input("Enter max number of Reels to fetch [Default: 5]: ").strip()
            limit_val = int(limit) if limit.isdigit() else 5
            print(f"[*] Processing Reels query matching profile trace target: {target}")
            reel_dl.download_user_reels(target, limit=limit_val)
        elif choice == "5":
            target = config.get("target_username", "sarmistha8939")
            print(f"[*] Processing Story streams tracking target: {target}")
            story_dl.download_user_stories(target)
        elif choice == "6":
            template = config.get("comment_template", "")
            preview = template.format(username=my_username)
            print("\n--- COMMENT TEXT PREVIEW ---")
            print(preview)
            print("----------------------------")
        elif choice == "7":
            rec_file = Path("download_record.txt")
            if rec_file.exists():
                print(rec_file.read_text(encoding="utf-8")[-2000:])
            else:
                print("[!] No processing transaction records discovered on local disk partitions.")
        elif choice == "8":
            log_file = Path("logs/instagram.log")
            if log_file.exists():
                print(log_file.read_text(encoding="utf-8")[-2000:])
            else:
                print("[!] No platform system log files generated yet.")
        elif choice == "9":
            print("[*] Terminating execution layers safely. Goodbye.")
            sys.exit(0)
        else:
            print("[-] Choice outside available operating boundaries. Re-enter options.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Execution interrupted by terminal console user operator commands. Exiting safely.")
        sys.exit(0)
