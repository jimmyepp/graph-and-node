import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/main_js.js"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    js = f.read()

target_classes = ["js-locations-component", "js-related-doctors", "js-locations-status"]

print("--- Searching for targeted classes in main.js ---")
for cls in target_classes:
    positions = [m.start() for m in re.finditer(re.escape(cls), js)]
    print(f"Class '{cls}' found {len(positions)} times.")
    for pos in positions[:3]:
        start = max(0, pos - 100)
        end = min(len(js), pos + 250)
        snippet = js[start:end].replace('\n', ' ')
        print(f"  Snippet at char {pos}: ... {snippet} ...")
