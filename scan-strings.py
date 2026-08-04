# -*- coding: utf-8 -*-
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
base = r"C:/Users/super/AppData/Roaming/npm/node_modules/@earendil-works/pi-coding-agent/dist/modes/interactive/components"
for f in ["tree-selector.js", "config-selector.js", "scoped-models-selector.js", "session-selector-search.js", "user-message-selector.js"]:
    t = open(base + "/" + f, encoding="utf-8").read()
    print("====", f)
    for m in re.finditer(r'["\x60]((?:[^"\\\x60]|\\.){4,90})["\x60]', t):
        s = m.group(1)
        if re.search(r"[A-Za-z]", s) and s[0:1].isupper() and "://" not in s and "/dist/" not in s and s != "UTF-8":
            print("  ", s)
