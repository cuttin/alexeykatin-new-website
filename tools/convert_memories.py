"""Convert the 24 kept posts of the static japanforayear mirror into Astro content entries.
Each post -> web/src/content/memories/<stem>/index.md plus its photos (01.jpg, 02.jpg, ...) beside it.
Source mirror is read only."""
import html
import pathlib
import re
import shutil
import struct
import sys
import urllib.parse
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding="utf-8")
SRC = pathlib.Path("C:/Users/alexe/Documents/japanforayear-static/site")
OUT = pathlib.Path("C:/Users/alexe/Documents/alexeykatin-site/web/src/content/memories")

# date, title, stem, category (same list as the approved timeline mockup)
POSTS = [
    ("2021-04-16", "Как купить машину в США. Мой опыт из Северной Каролины", "kak-kupit-mashinu-v-ssha-moj-opy-t-iz-severnoj-karoliny", "Полезное"),
    ("2017-06-10", "Футбол ака соккер в Северной Каролине", "futbol-aka-sokker-v-severnoj-karoline", "США"),
    ("2017-06-06", "Нью-Йорк в мае", "n-yu-jork-v-mae", "США"),
    ("2017-01-24", "Работа на открытом воздухе. Эстуарий реки Ньюс", "rabota-na-otkry-tom-vozduhe-e-stuarij-reki-n-yus", "США"),
    ("2015-06-08", "Хирошима и Миядзима", "hiroshima-i-miyadzima", "Япония"),
    ("2015-05-30", "Окинава. Дождливая поездка в самую южную часть Японии", "okinava-dozhdlivaya-poezdka-v-samuyu-yuzhnuyu-chast-yaponii", "Япония"),
    ("2015-05-18", "Поездка в Ниими: немного пещер", "poezdka-v-niimi-nemnogo-peshher", "Япония"),
    ("2015-04-07", "Вьетнам: Нячанг и Хошимин", "vietnam-nyachang-i-hoshimin", "Азия"),
    ("2015-03-11", "Дорога во Вьетнам из Окаямы", "doroga-vo-v-etnam-iz-okayamy", "Азия"),
    ("2015-03-06", "Небольшое азиатское турне", "nebol-shoe-aziatskoe-turne", "Азия"),
    ("2015-01-09", "Немного о Японии: стиль и одежда японцев", "nemnogo-o-yaponii-stil-i-odezhda-yapontsev", "Япония"),
    ("2014-12-19", "Немного о японцах и Японии", "nemnogo-o-yapontsah-i-yaponii", "Япония"),
    ("2014-11-27", "Осенний рынок в Такебе, Юбара онсен", "osennij-ry-nok-v-takebe-yubara-onsen", "Япония"),
    ("2014-11-19", "Остров Хонжима, порт Конжима. Рыбалка и велопрогулка", "ostrov-honzhima-port-konzhima-ry-balka-i-veloprogulka", "Япония"),
    ("2014-11-03", "Середина и конец октября: мост Сэто и немного Окаямы", "seredina-i-konets-oktyabrya-most-se-to-i-nemnogo-okayamy", "Япония"),
    ("2014-10-13", "Поездка в Курашики", "poezdka-v-kurashiki", "Япония"),
    ("2014-10-06", "Первые впечатления от университета Окаямы", "pervy-e-vpechatleniya-ot-universiteta-okayamy", "Япония"),
    ("2014-10-02", "Переезд и первые дни в Окаяме", "pereezd-i-pervy-e-dni-v-okayame", "Япония"),
    ("2014-09-30", "Аквариум Осаки Каюкан", "akvarium-osaki-kayukan", "Япония"),
    ("2014-09-29", "Киото", "kioto", "Япония"),
    ("2014-09-27", "Замок Осаки и Небоскреб Умеда", "zamok-osaki-i-neboskreb-umeda", "Япония"),
    ("2014-09-26", "Первый день: небольшая прогулка по Осаке", "pervy-j-den-nebol-shaya-progulka-po-osake", "Япония"),
    ("2014-09-25", "Дорога в Японию: перелет и первая остановка", "doroga-v-yaponiyu-perelet-i-pervaya-ostanovka", "Япония"),
    ("2014-09-16", "Предыстория: как и почему я еду в Японию", "predystoriya_pochemu_ya_edu_v_yaponiu", "Япония"),
]
KEPT = {p[2] for p in POSTS}
IMG_HOSTS = ("fotki.yandex.ru", "img-fotki.yandex.ru")


def md_escape(t):
    t = t.replace("\\", "\\\\")
    t = re.sub(r"([*_\[\]`])", r"\\\1", t)
    return t.replace("<", "&lt;")


def reset_orientation(path):
    """The 10 photos that carry an EXIF Orientation tag are already upright in pixels (checked on a contact sheet,
    2026-11-10); the tag would turn them sideways in the build, so set it to 1 in the copy."""
    b = bytearray(path.read_bytes())
    i = b.find(b"Exif\x00\x00")
    if i < 0:
        return
    t = i + 6
    e = "<" if b[t:t + 2] == b"II" else ">"
    off = t + struct.unpack(e + "I", b[t + 4:t + 8])[0]
    for k in range(struct.unpack(e + "H", b[off:off + 2])[0]):
        ent = off + 2 + 12 * k
        if struct.unpack(e + "H", b[ent:ent + 2])[0] == 0x112:
            if struct.unpack(e + "H", b[ent + 8:ent + 10])[0] != 1:
                b[ent + 8:ent + 10] = struct.pack(e + "H", 1)
                path.write_bytes(b)
            return


def fix_href(h):
    """Internal post links -> /memories/<stem>/; links to dropped pages -> None (text kept)."""
    u = urllib.parse.urlparse(h)
    if u.netloc in ("", "japanforayear.ru", "www.japanforayear.ru"):
        m = re.fullmatch(r"/([^/]+)\.html", u.path)
        if m and m.group(1) in KEPT:
            return f"/memories/{m.group(1)}/"
        return None
    if h.startswith("//"):
        return "https:" + h
    return h


class Post(HTMLParser):
    def __init__(self, stem, outdir):
        super().__init__(convert_charrefs=True)
        self.stem, self.outdir = stem, outdir
        self.blocks, self.cur = [], []
        self.links = []          # stack: href or None per open <a>
        self.n_img, self.missing, self.skip = 0, [], 0

    def flush(self):
        t = "".join(self.cur).strip()
        t = re.sub(r"[ \t]*\\\n[ \t]*", "\\\n", t)
        t = re.sub(r"(\\\n)+$", "", t)
        if t:
            # a line starting like "1." or "-" would become a list; keep it as text
            t = re.sub(r"(?m)^(\d+)\.(\s)", r"\1\\.\2", t)
            t = re.sub(r"(?m)^([-+>#])", r"\\\1", t)
            self.blocks.append(t)
        self.cur = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if self.skip:
            if tag == "div":
                self.skip += 1
            return
        if tag == "div" and "addtoany" in (a.get("class") or ""):
            self.skip = 1
        elif tag == "p":
            self.flush()
        elif tag == "br":
            # the old posts use <br> as a paragraph break
            self.flush()
        elif tag == "strong" or tag == "b":
            self.cur.append("**")
        elif tag == "a":
            h = a.get("href") or ""
            host = urllib.parse.urlparse(h).netloc
            href = None if host in IMG_HOSTS else fix_href(h)
            self.links.append(href)
            if href:
                self.cur.append("[")
        elif tag == "img":
            p = SRC / urllib.parse.unquote(a["src"]).lstrip("/")
            if not p.exists():
                self.missing.append(a["src"])
                return
            self.n_img += 1
            name = f"{self.n_img:02d}{p.suffix.lower() or '.jpg'}"
            shutil.copyfile(p, self.outdir / name)
            reset_orientation(self.outdir / name)
            self.flush()
            self.blocks.append(f"![](./{name})")
        elif tag == "iframe":
            self.flush()
            src = a["src"]
            if src.startswith("//"):
                src = "https:" + src
            self.blocks.append(f'<div class="video"><iframe src="{html.escape(src)}" loading="lazy" allowfullscreen title="Видео"></iframe></div>')

    def handle_endtag(self, tag):
        if self.skip:
            if tag == "div":
                self.skip -= 1
            return
        if tag == "p":
            self.flush()
        elif tag in ("strong", "b"):
            self.cur.append("**")
        elif tag == "a" and self.links:
            href = self.links.pop()
            if href:
                self.cur.append(f"]({href})")

    def handle_data(self, d):
        if not self.skip:
            self.cur.append(md_escape(re.sub(r"\s+", " ", d)))


OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.iterdir():
    shutil.rmtree(old)
total_img, report = 0, []
for date, title, stem, cat in POSTS:
    s = (SRC / f"{stem}.html").read_text(encoding="utf-8")
    body = re.search(r'(?s)<div class="entry-content[^>]*>(.*?)<!-- \.entry-content -->', s).group(1)
    d = OUT / stem
    d.mkdir(parents=True)
    p = Post(stem, d)
    p.feed(body)
    p.flush()
    text = "\n\n".join(b.replace("****", "") for b in p.blocks if b not in ("**", "****"))
    fm = [f'title: "{title}"', f"date: {date}", f"category: {cat}"]
    if p.n_img:
        fm.append("cover: ./01" + next((x.suffix for x in sorted(d.iterdir()) if x.name.startswith("01")), ".jpg"))
    (d / "index.md").write_text("---\n" + "\n".join(fm) + "\n---\n\n" + text + "\n", encoding="utf-8")
    total_img += p.n_img
    report.append(f"{stem}: {p.n_img} img, {len(p.blocks)} blocks, missing {len(p.missing)}")
print("\n".join(report))
print("posts", len(POSTS), "images", total_img)
