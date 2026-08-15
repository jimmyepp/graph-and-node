import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/raw_ross_breast_center.html"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Regex to find all script tags and their contents
script_pattern = re.compile(r'<script([^>]*)>([\s\S]*?)</script>', re.IGNORECASE)
matches = script_pattern.findall(html)

print(f"Analyzing {len(matches)} script tags:\n")

for i, (attrs, body) in enumerate(matches, 1):
    src_match = re.search(r'src=["\'](.*?)["\']', attrs, re.IGNORECASE)
    src = src_match.group(1) if src_match else None
    
    if src:
        print(f"[{i}] External Script: {src}")
        if "defer" in attrs.lower():
            print("    - Status: Defer")
        elif "async" in attrs.lower():
            print("    - Status: Async")
        else:
            print("    - Status: Blocking (Normal)")
    else:
        print(f"[{i}] Inline Script (Length: {len(body)} chars)")
        print("    Body preview (first 400 chars):")
        print("    " + "\n    ".join(body.strip().split("\n")[:10]))
    print("-" * 50)
