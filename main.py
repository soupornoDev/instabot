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
    print("1. Login to Instagram (Dynamic Username)")
    print("2. Validate Saved Session")
    print("3. Download Posts")
    print("4. Download Reels")
    print("5. Download Accessible Stories")
    print("6. Preview Comment Text")
    print("7. View Download Records")
    print("8. View Application Logs")
    print("9. Exit")
    print("="*40)

def parse_limit() -> int:
    limit_input = input("Enter max number to fetch [Type * for ALL, or Enter for 5]: ").strip()
    if limit_input == '*':
        return 0
    if limit_input.isdigit():
        return int(limit_input)
    return 5

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
    
    while True:
        print_menu()
        choice = input("Select an option (1-9): ").strip()
        
        if choice == "9":
            print("[*] Terminating execution layers safely. Goodbye.")
            sys.exit(0)
            
        # Intercept actions if user is not authenticated yet
        if choice in ["3", "4", "5", "6"]:
            if not auth_mgr.is_logged_in():
                print("[!] Access Denied. No active authenticated session found.")
                login_now = input("Would you like to login right now? (y/n): ").strip().lower()
                if login_now == 'y':
                    user_to_login = input("Enter YOUR Instagram Username to authenticate: ").strip()
                    if auth_mgr.login(user_to_login):
                        print(f"[+] Login successful as {user_to_login}. Proceeding to action.")
                    else:
                        print("[-] Login failed. Action aborted.")
                        continue
                else:
                    print("[-] Action cancelled.")
                    continue

        if choice == "1":
            user_to_login = input("Enter YOUR Instagram Username to authenticate: ").strip()
            if auth_mgr.login(user_to_login):
                print(f"[+] Successfully authenticated as {user_to_login}")
            else:
                print("[-] Authentication flow processing failed.")
                
        elif choice == "2":
            # Quick login check
            user_to_check = input("Enter Username to check session state: ").strip()
            auth_mgr.load_session(user_to_check)
            if auth_mgr.validate_session():
                print(f"[+] Active session for {user_to_check} validated successfully.")
            else:
                print(f"[-] Session for {user_to_check} is invalid or expired.")
                
        elif choice == "3":
            target = input("Enter TARGET Username to download posts from: ").strip()
            limit_val = parse_limit()
            print(f"[*] Querying posts from target: {target}")
            post_dl.download_user_posts(target, limit=limit_val)
            
        elif choice == "4":
            target = input("Enter TARGET Username to download Reels from: ").strip()
            limit_val = parse_limit()
            print(f"[*] Querying Reels from target: {target}")
            reel_dl.download_user_reels(target, limit=limit_val)
            
        elif choice == "5":
            target = input("Enter TARGET Username to download Stories from: ").strip()
            print(f"[*] Querying Stories from target: {target}")
            story_dl.download_user_stories(target)
            
        elif choice == "6":
            template = config.get("comment_template", "")
            preview = template.format(username=auth_mgr.current_username)
            print("\n--- COMMENT TEXT PREVIEW ---")
            print(preview)
            print("----------------------------")
            
        elif choice == "7":
            rec_file = Path("download_record.txt")
            if rec_file.exists():
                print(rec_file.read_text(encoding="utf-8")[-2000:])
            else:
                print("[!] No records found.")
                
        elif choice == "8":
            log_file = Path("logs/instagram.log")
            if log_file.exists():
                print(log_file.read_text(encoding="utf-8")[-2000:])
            else:
                print("[!] No logs found.")
        else:
            if choice != "9":
                print("[-] Invalid input option.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Interrupted. Exiting.")
        sys.exit(0)
