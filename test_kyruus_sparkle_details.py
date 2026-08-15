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
        print(f"Found {len(providers)} providers matching 'sparkle':")
        for i, provider in enumerate(providers, 1):
            print(f"\n[{i}] Name: {provider.get('name')}")
            print(f"    Specialty: {provider.get('specialty')}")
            # Look for 'sparkle' in the provider dict keys and values (ignoring the 'imageUrl' which always contains sparkle-assets)
            for k, v in provider.items():
                if k != "imageUrl" and v and "sparkle" in str(v).lower():
                    print(f"    Field '{k}' contains 'sparkle':")
                    print(f"      {str(v)[:300]}")
except Exception as e:
    print(f"Error: {e}")
