import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.christushealth.org/assets/js/main.js?v=639131915580000000"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=20) as response:
        js_content = response.read().decode('utf-8', errors='ignore')
        with open("/Users/jimmyepperson/Developer/GraphandNode/main_js.js", "w", encoding="utf-8") as f:
            f.write(js_content)
        print(f"main.js downloaded successfully. Size: {len(js_content) / 1024:.2f} KB")
except Exception as e:
    print(f"Error fetching main.js: {e}")
