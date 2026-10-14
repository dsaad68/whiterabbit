import json, re, sys, importlib.util
spec = importlib.util.spec_from_file_location("content", sys.argv[1]); c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
p = sys.argv[2]
s = open(p, encoding="utf-8").read()
block = ("/* CONTENT:BEGIN · the words of the page, written from the fact-checked research (sources in DATA.sources) */\n"
         "const CONTENT_UI = " + json.dumps(c.UI, ensure_ascii=False, indent=1) + ";\n"
         "for (const l of Object.keys(CONTENT_UI)) Object.assign(UI[l], CONTENT_UI[l]);\n"
         "const DATA = " + json.dumps(c.DATA, ensure_ascii=False, indent=1) + ";\n"
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
