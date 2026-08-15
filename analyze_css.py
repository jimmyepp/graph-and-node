import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/raw_ross_breast_center.html"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

stylesheets = re.findall(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', html, re.IGNORECASE)
print(f"Total stylesheets: {len(stylesheets)}")
for css in stylesheets:
    print(css)
