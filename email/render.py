"""Scény e-mailu (sceny.html) -> obrázky 2× do static/email/ (build je zkopíruje do dist/email/).

    python3 email/render.py
"""
import functools, http.server, io, os, re, socketserver, threading
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static", "email")
PORT = 8791

FLOTILA = ["porsche-gt4-mr", "audi-r8", "mercedes-amg-g63", "bmw-m4-cabrio", "audi-rs6", "dodge-challenger"]
JPG = ["svetla", "hero", "cyber", "m2", "amg", "poukaz", "brana"] + [f"f-{a}" for a in FLOTILA]
PNG = ["logo-bile", "logo-tmave"]


def stranka():
    s = open(os.path.join(ROOT, "email", "sceny.html"), encoding="utf-8").read()
    svetla = open(os.path.join(ROOT, "src", "_svetylka.html"), encoding="utf-8").read()
    dl = "".join(
        f'<div class="sc krem" id="f-{a}" style="width:264px;height:150px"><div class="dl" style="position:absolute;inset:0">'
        f'<span class="stin"></span><img class="vuz" src="../img/auta/{a}.webp" alt=""></div></div>' for a in FLOTILA)
    s = s.replace("__SVETYLKA__", svetla).replace("__FLOTILA__", dl)
    with open(os.path.join(ROOT, "email", "_sceny_render.html"), "w", encoding="utf-8") as f:
        f.write(s)


def main():
    stranka()
    os.makedirs(OUT, exist_ok=True)
    class Tichy(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), functools.partial(Tichy, directory=ROOT)) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 800, "height": 1200}, device_scale_factor=2)
            pg.goto(f"http://127.0.0.1:{PORT}/email/_sceny_render.html", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            for id_ in JPG:
                png = pg.locator(f"#{id_}").screenshot()
                im = Image.open(io.BytesIO(png)).convert("RGB")
                im.save(os.path.join(OUT, f"{id_}.jpg"), quality=82, optimize=True, progressive=True)
            for id_ in PNG:
                pg.locator(f"#{id_}").screenshot(path=os.path.join(OUT, f"{id_}.png"), omit_background=True)
            b.close()
        srv.shutdown()
    os.remove(os.path.join(ROOT, "email", "_sceny_render.html"))
    for f in sorted(os.listdir(OUT)):
        print(f"{f:28} {os.path.getsize(os.path.join(OUT, f)) // 1024:5} kB  {Image.open(os.path.join(OUT, f)).size}")


if __name__ == "__main__":
    main()
