import re
from pathlib import Path

html = Path(__file__).with_name("index.html").read_text(encoding="utf-8")
used = set(re.findall(r'data-i18n(?:-placeholder|-aria)?="([^"]+)"', html))
print("USED KEYS", len(used))


def keys_for(lang: str) -> set[str]:
    mm = re.search(rf"{lang}: \{{(.*?)\n      \}},", html, re.S)
    if not mm:
        print("NO BLOCK", lang)
        return set()
    return set(re.findall(r"^\s+([A-Za-z0-9_]+):", mm.group(1), re.M))


kz, en, ru = keys_for("kz"), keys_for("en"), keys_for("ru")
print("kz", len(kz), "en", len(en), "ru", len(ru))
print("kz-en", sorted(kz - en), "count", len(kz - en))
print("kz-ru", sorted(kz - ru), "count", len(kz - ru))
print("en-kz", sorted(en - kz), "count", len(en - kz))
print("used-kz", sorted(used - kz))
print("kz-used", sorted(kz - used))
