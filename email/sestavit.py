"""sablona.html -> mail.html (obrázky z webu, k odeslání) + nahled.html (místní obrázky).

    python3 email/sestavit.py [--img https://…/email/] [--odkaz https://dreamrental-poukazy.eu/]
"""
import argparse, os

ROOT = os.path.dirname(os.path.abspath(__file__))
FLOTILA = [("porsche-gt4-mr", "Porsche", "Cayman GT4 MR"), ("audi-r8", "Audi", "R8"),
           ("mercedes-amg-g63", "Mercedes-AMG", "G63"), ("bmw-m4-cabrio", "BMW", "M4 Cabrio"),
           ("audi-rs6", "Audi", "RS6"), ("dodge-challenger", "Dodge", "Challenger")]
UTM = "?utm_source=email&utm_medium=email&utm_campaign=poukazy-vanoce"


def flotila():
    bunka = ('<td width="50%" valign="top" style="padding:0 {pr}px 18px {pl}px">'
             '<a href="{{{{LINK}}}}" style="display:block"><img src="{{{{IMG}}}}f-{id}.jpg" width="264" alt="{z} {m}" '
             'style="width:100%;height:auto;border-radius:18px"></a>'
             '<p class="f-t" style="margin:10px 0 0 4px;font-family:\'Inter\',Helvetica,Arial,sans-serif;font-size:11px;line-height:14px;'
             'letter-spacing:.08em;text-transform:uppercase;color:#8f877d">{z}</p>'
             '<p class="f-d" style="margin:2px 0 0 4px;font-family:\'Outfit\',Helvetica,Arial,sans-serif;font-size:17px;line-height:22px;'
             'font-weight:500;color:#0f1218">{m}</p></td>')
    radky = []
    for i in range(0, len(FLOTILA), 2):
        a, b = FLOTILA[i], FLOTILA[i + 1]
        radky.append("<tr>" + bunka.format(id=a[0], z=a[1], m=a[2], pl=0, pr=8)
                     + bunka.format(id=b[0], z=b[1], m=b[2], pl=8, pr=0) + "</tr>")
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
            + "".join(radky) + "</table>")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--img", default="https://webhunter-navrhy.github.io/dreamrental-poukazy/email/")
    ap.add_argument("--odkaz", default="https://dreamrental-poukazy.eu/")
    a = ap.parse_args()
    s = open(os.path.join(ROOT, "sablona.html"), encoding="utf-8").read().replace("{{FLOTILA}}", flotila())
    odkaz = a.odkaz + UTM
    for nazev, img in (("mail.html", a.img), ("nahled.html", "../static/email/")):
        with open(os.path.join(ROOT, nazev), "w", encoding="utf-8") as f:
            f.write(s.replace("{{IMG}}", img).replace("{{LINK}}", odkaz))
    print(f"mail.html {os.path.getsize(os.path.join(ROOT, 'mail.html')) // 1024} kB (Gmail ořezává nad 102 kB)")


if __name__ == "__main__":
    main()
