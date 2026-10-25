import json, re, sys, importlib.util
spec = importlib.util.spec_from_file_location("content", sys.argv[1]); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
p = sys.argv[2]
s = open(p, encoding="utf-8").read()

# ---- typesetting pass over every string that the page inserts as HTML ----
# en/de: no-break space between a number and its unit and inside some Chinese names,
#        CJK runs marked lang="zh-Hans", the German Beuys title in English text marked lang="de".
# zh:    a number and its unit kept on one line with <span class="nw">.
# Left alone: URLs, icon/colour keys, the year/when/v display values, the counted gift.kg,
# the flavour names and notes (set with textContent) and the UI keys used as attributes.
NBSP = " "
LANGS = ("en", "de", "zh")
SKIP_KEYS = {"url", "icon", "band", "end", "count", "year", "when", "v", "kinds"}
SKIP_UI = lambda k: k == "gift.kg" or k == "glass.drop" or k.startswith("a11y.")

UNITS = ("cm|mm|km|kg|g|t|ml|kJ|kcal|m|"
         "grams?|kilos?|kilograms?|kilocalories|tonnes?|tons?|metres?|seconds?|minutes?|hours?|days?|"
         "million|billion|yuan|jin|dollars?|"
         "Gramm|Kilo|Kilogramm|Kilokalorien|Tonnen?|Meter|Sekunden?|Minuten?|Stunden?|Tage?n?|"
         "Millionen|Milliarden|Yuan|Jin|US-Dollar|Euro|Stück|Prozent|%")
WORDNUM = ("one two three four five six seven eight nine ten twelve twenty "
           "eine zwei drei vier fünf sechs sieben acht neun zehn zwölf zwanzig").split()
AFTER_NUM = "|".join([r"(?<=\d)", r"(?<=\d\+)", r"(?<=\d-plus)"] +
                     [r"(?<=\b" + w + ")" for n in WORDNUM for w in (n, n.capitalize())])  # lookbehinds must be fixed-width
EN_DE_NB = [
    # 5 g, 27,000 tonnes, 0,02 mm, 250+ kg, 500-plus jin, four hours, Vier Tonnen; ≈ 5; US$ 40; 400 million yuan
    re.compile(r"(?:" + AFTER_NUM + r") (?=(?:" + UNITS + r")(?![\w-]))"),
    re.compile(r"(?<=≈) (?=\d)"),
    re.compile(r"(?<=US\$) (?=\d)"),
    re.compile(r"(?:(?<=\bmillion)|(?<=\bbillion)|(?<=\bMillionen)|(?<=\bMilliarden)) (?=(?:yuan|Yuan|kilos|Kilo|tonnes|Tonnen|dollars|US-Dollar)\b)"),
]
NAMES = ("Lu Xiuqin", "Zhou Enlai", "Feng Boyong", "Liu Yiqing")
HAN = r"㐀-䶿一-鿿豈-﫿"
CJK_RUN = re.compile("[" + HAN + "]+(?:[　-〿＀-￯·]+[" + HAN + "]+)*")
DE_TITLE = re.compile(r"Chinesischer Hasenzucker")
ZH_UNITS = "兔年|毫米|厘米|千卡|千焦|公斤|毫升|小时|分钟|世纪|美元|年代|个月|年|月|日|号|克|吨|斤|秒|杯|颗|种|份|套|件|岁|米(?!老鼠)|个|元|届|天|周"
ZH_NUM = r"\d+(?:[.,]\d+)*(?:[万亿][多余]?(?:" + ZH_UNITS + r")?|[多余]?(?:" + ZH_UNITS + r"))"
ZH_NW = re.compile(ZH_NUM + r"(?:" + ZH_NUM + r")*")
TAG = re.compile(r"(<[^>]*>)")

def text_parts(html, fn):
    """Apply fn to the text between tags only; text already inside a marked span is left as is."""
    out, marked = [], []          # marked: one flag per open <span>, True if it already carries lang/nw
    for part in TAG.split(html):
        if part.startswith("<"):
            if re.match(r"<span\b", part):
                marked.append(bool(re.search(r'\blang=|class="nw"', part)))
            elif part.startswith("</span") and marked:
                marked.pop()
            out.append(part)
        elif part:
            out.append(part if any(marked) else fn(part))
    return "".join(out)

def en_de(text, lang):
    for rx in EN_DE_NB: text = rx.sub(NBSP, text)
    for n in NAMES: text = text.replace(n, n.replace(" ", NBSP))
    text = CJK_RUN.sub(lambda m: '<span lang="zh-Hans">' + m.group(0) + "</span>", text)
    if lang == "en": text = DE_TITLE.sub(lambda m: '<span lang="de">' + m.group(0) + "</span>", text)
    return text

def zh(text):
    return ZH_NW.sub(lambda m: '<span class="nw">' + m.group(0) + "</span>", text)

def typeset(o, lang=None):
    if isinstance(o, dict):
        return {k: (v if k in SKIP_KEYS else typeset(v, k if k in LANGS else lang)) for k, v in o.items()}
    if isinstance(o, list): return [typeset(v, lang) for v in o]
    if isinstance(o, str) and lang in ("en", "de"): return text_parts(o, lambda t: en_de(t, lang))
    if isinstance(o, str) and lang == "zh": return text_parts(o, zh)
    return o

UI = {l: {k: (v if SKIP_UI(k) else typeset(v, l)) for k, v in keys.items()} for l, keys in c.UI.items()}
DATA = typeset(c.DATA)
dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1).replace(NBSP, "\\u00a0")  # visible in the source

block = ("/* CONTENT:BEGIN · the words of the page, written from the fact-checked research (sources in DATA.sources) */\n"
         "const CONTENT_UI = " + dump(UI) + ";\n"
         "for (const l of Object.keys(CONTENT_UI)) Object.assign(UI[l], CONTENT_UI[l]);\n"
         "const DATA = " + dump(DATA) + ";\n"
         "/* CONTENT:END */")
if "/* CONTENT:BEGIN" in s:
    s = re.sub(r"/\* CONTENT:BEGIN.*?/\* CONTENT:END \*/", lambda m: block, s, flags=re.S)
else:
    a = s.index("const DATA = {   /* PROVISIONAL")
    end_marker = 'UI.en["foot.disc"] = "Fan page, not affiliated with the maker.";'
    b = s.index(end_marker) + len(end_marker)
    s = s[:a] + block + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("injected", len(block), "chars")
