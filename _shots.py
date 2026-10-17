import subprocess
from pathlib import Path

browser = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out = Path(r"C:\Users\aomar\Desktop\batyrlar-preview")
src = Path(r"C:\Users\aomar\Desktop\Сайт военный центр\index.html")
out.mkdir(exist_ok=True)
html = src.read_text(encoding="utf-8")
(out / "index.html").write_text(html, encoding="utf-8")
extra = """
<script>
window.addEventListener("load", function () {
  var result = {};
  ["kz","en","ru"].forEach(function (l) {
    document.querySelector('[data-lang="' + l + '"]').click();
    result[l] = {
      cta: document.querySelector('[data-i18n="ctaEnroll"]').textContent,
      badge: document.querySelector('[data-i18n="heroBadge"]').textContent,
      about: document.querySelector('[data-i18n="navAbout"]').textContent,
      htmlLang: document.documentElement.lang,
      stored: localStorage.getItem("batyrlar-lang")
    };
  });
  document.querySelector('[data-lang="kz"]').click();
  var pre = document.createElement("pre");
  pre.id = "i18n-test";
  pre.textContent = JSON.stringify(result);
  document.body.appendChild(pre);
});
</script>
"""
(out / "index.test.html").write_text(html + extra, encoding="utf-8")
base = (out / "index.html").as_uri()
test = (out / "index.test.html").as_uri()

for name, w, h in [("desktop.png", 1440, 900), ("mobile.png", 390, 844), ("full.png", 1440, 4200)]:
    dest = out / name
    cmd = [
        browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--allow-file-access-from-files", f"--window-size={w},{h}",
        f"--screenshot={dest}", base,
    ]
    subprocess.run(cmd, check=True)
    print("shot", name, dest.stat().st_size)

cmd = [
    browser, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
    "--virtual-time-budget=8000", "--dump-dom", test,
]
r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
text = r.stdout
marker = 'id="i18n-test"'
i = text.find(marker)
print("FOUND_TEST", i >= 0)
if i >= 0:
    start = text.find(">", i) + 1
    end = text.find("</pre>", start)
    (out / "i18n-result.json").write_text(text[start:end], encoding="utf-8")
    print("WROTE i18n-result.json")
else:
    print("DOM_LEN", len(text))
    print(text[-2000:])
    print("STDERR", r.stderr[-1000:] if r.stderr else "")
