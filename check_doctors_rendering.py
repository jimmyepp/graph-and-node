import re

file_path = "/Users/jimmyepperson/Developer/GraphandNode/raw_ross_breast_center.html"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Let's search for the js-doctors-items container
match = re.search(r'class=["\'][^"\']*js-doctors-items[^"\']*["\'][\s\S]*?>([\s\S]*?)</div', html, re.IGNORECASE)
if match:
    content = match.group(1).strip()
    print("Found container 'js-doctors-items'!")
    print(f"Container content length: {len(content)} characters.")
    print(f"Container content: '{content[:500]}'")
else:
    print("js-doctors-items container not found by class search.")
    # Let's look for any mentions of doctors in that section
    related_section = re.search(r'<section[^>]+class=["\'][^"\']*js-related-doctors[^"\']*["\'][\s\S]*?></section>', html, re.IGNORECASE)
    if related_section:
        print("Found related section, but it is empty/closed immediately or check details:")
        print(related_section.group(0))
    else:
        # Let's search for sections with name="Related Doctors"
        sec = re.search(r'<section[^>]+name=["\']Related Doctors["\'][\s\S]*?>([\s\S]*?)</section>', html, re.IGNORECASE)
        if sec:
            print("Found section by name 'Related Doctors':")
            body = sec.group(1).strip()
            print(f"Body length: {len(body)} characters.")
            print(f"Body snippet: {body[:1000]}")
        else:
            print("Section 'Related Doctors' not found.")
