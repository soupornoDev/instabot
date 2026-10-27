# Instagram Media Manager

## Termux Setup
```bash
pkg update && pkg upgrade -y
pkg install python libjpeg-turbo unzip clang make -y
termux-setup-storage
unzip instagram_media_manager.zip
cd instagram-media-manager
pip install -r requirements.txt
python main.py
```
