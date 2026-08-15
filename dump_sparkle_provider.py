import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.christushealth.org/api/sitecore/kyruus/search"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

data = json.dumps({"keyword": "sparkle"}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
        body = response.read().decode('utf-8', errors='ignore')
        parsed = json.loads(body)
        providers = parsed.get("providers", [])
        if providers:
            print(json.dumps(providers[0], indent=2))
except Exception as e:
    print(f"Error: {e}")
