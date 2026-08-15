import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/main_js.js"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    js = f.read()

# Let's search for references to API_ENDPOINTS properties
keywords = ["GetProviderData", "Locations", "providers", "locations", "allTaxons", "Taxonomy"]

print("--- Searching for API endpoint calls in main.js ---")
for kw in keywords:
    # Find positions of keyword
    positions = [m.start() for m in re.finditer(re.escape(kw), js)]
    print(f"Keyword '{kw}' found {len(positions)} times.")
    for pos in positions[:3]:
        # Print snippet of 200 characters around the position
        start = max(0, pos - 100)
        end = min(len(js), pos + 250)
        snippet = js[start:end].replace('\n', ' ')
        print(f"  Snippet at char {pos}: ... {snippet} ...")

# Let's check for ajax / fetch calls
print("\n--- AJAX / Fetch Calls Search ---")
ajax_calls = len(re.findall(r'\$\.ajax', js))
fetch_calls = len(re.findall(r'\bfetch\(', js))
print(f"Total $.ajax calls: {ajax_calls}")
print(f"Total fetch() calls: {fetch_calls}")
