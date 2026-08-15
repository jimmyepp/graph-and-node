import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/raw_ross_breast_center.html"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Let's search for keywords related to loading overlays
loading_keywords = ["loader", "loading", "spinner", "overlay", "shimmer", "preloader"]
for kw in loading_keywords:
    matches = re.findall(r'<div[^>]+(?:id|class)=["\'][^"\']*{0}[^"\']*["\'][^>]*>'.format(kw), html, re.IGNORECASE)
    if matches:
        print(f"Found matches for keyword '{kw}':")
        for m in matches[:5]:
            print("  ", m)
