import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/raw_ross_breast_center.html"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

classes_to_check = [
    "js-providers-locations-list",
    "js-providers-locations-list-fad",
    "js-providers-locations",
    "js-providers",
    "js-locations",
    "js-gallery"
]

print("--- Checking elements by class in raw HTML ---")
for cls in classes_to_check:
    matches = re.findall(r'<[^>]+class=["\'][^"\']*{0}[^"\']*["\'][^>]*>'.format(cls), html, re.IGNORECASE)
    print(f"Class '{cls}' found {len(matches)} times.")
    for m in matches[:3]:
        print("  ", m)
