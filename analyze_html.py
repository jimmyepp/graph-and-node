import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/raw_ross_breast_center.html"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

print(f"Total HTML File Size: {len(html) / 1024:.2f} KB ({len(html)} bytes)")

print("\n--- 1. Meta Robots Tags ---")
robots = re.findall(r'<meta[^>]+name=["\']robots["\'][^>]*>', html, re.IGNORECASE)
for r in robots:
    print(r)
if not robots:
    print("No meta robots tag found.")

print("\n--- 2. Canonical Tags ---")
canonicals = re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]*>', html, re.IGNORECASE)
for c in canonicals:
    print(c)
if not canonicals:
    print("No canonical link found.")

print("\n--- 3. Page Title & OG Tags ---")
title = re.findall(r'<title>(.*?)</title>', html, re.IGNORECASE)
print(f"Title: {title}")
og_tags = re.findall(r'<meta[^>]+property=["\']og:[^>]+>', html, re.IGNORECASE)
for og in og_tags[:5]:
    print(og)

print("\n--- 4. Static Content Check ---")
# Check if the actual content is in the raw HTML, or if it's dynamic
keywords_to_check = [
    "Ross Breast Center",
    "910 E. Houston",  # part of address
    "903-606-5433",     # phone number
    "Comprehensive Breast Care",
    "Mammography",
    "Tyler"
]
for kw in keywords_to_check:
    found = kw.lower() in html.lower()
    print(f"Contains '{kw}': {found}")

print("\n--- 5. Javascript & Script Imports (Count & Preview) ---")
scripts = re.findall(r'<script[^>]*>', html, re.IGNORECASE)
print(f"Total script tags in HTML: {len(scripts)}")

# Look for potential redirects or blocking scripts
print("\n--- 6. Inline Scripts of Interest ---")
# Let's extract any script containing window.API_ENDPOINTS or similar config
endpoint_scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html, re.IGNORECASE)
found_endpoints = False
for s in endpoint_scripts:
    if "API_ENDPOINTS" in s or "doctorlocations" in s or "kyruus" in s:
        found_endpoints = True
        print("Found API_ENDPOINTS script:")
        print(s.strip()[:1000])
        print("...")

if not found_endpoints:
    print("No API_ENDPOINTS config script found inline on this page.")
