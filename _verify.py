"""Headless verification of the Batyrlar landing page."""
import json
import os
import subprocess
import sys
from pathlib import Path

OUT = Path(r"C:\Users\aomar\Desktop\Сайт военный центр\_screens")
OUT.mkdir(exist_ok=True)
URL = "http://127.0.0.1:8765/"

candidates = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
browser = next((p for p in candidates if os.path.exists(p)), None)
print("BROWSER", browser)
if not browser:
    sys.exit("No Chrome/Edge found")

def shot(name, width, height):
    dest = OUT / name
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={dest}",
        URL,
    ]
    print("RUN", name)
    subprocess.run(cmd, check=True)
    print("OK", dest, dest.stat().st_size)

shot("desktop.png", 1440, 900)
shot("mobile.png", 390, 844)

# dump key texts via JS-less HTML parse
html = Path(r"C:\Users\aomar\Desktop\Сайт военный центр\index.html").read_text(encoding="utf-8")
assert 'lang="kk"' in html
assert "Тіркелу" in html
assert "localStorage" in html
assert "kz" in html and "en:" in html and "ru:" in html
assert "player.vimeo.com/video/1088756819" in html
assert "+7 700 100 0011" in html
assert "Аманжол Уразбаев" in html
print("STATIC CHECKS OK")
print(json.dumps({"desktop": str(OUT / "desktop.png"), "mobile": str(OUT / "mobile.png")}))
