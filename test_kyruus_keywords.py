import urllib.request
import urllib.error
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

payloads = {
    "cardiology": {"keyword": "Cardiology"},
    "sparkle": {"keyword": "sparkle"},
    "invalid": {"keyword": "SomeNonexistentKeywordXYZ"}
}

for name, payload in payloads.items():
    data = json.dumps(payload).encode('utf-8')
    print(f"\n--- Testing {name}: {payload} ---")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
            print(f"Status: {status}")
            print(f"Response Length: {len(body)} bytes")
            parsed = json.loads(body)
            if "providers" in parsed:
                providers = parsed["providers"]
                print(f"Success! Found {len(providers)} providers.")
                for provider in providers[:3]:
                    print(f" - Provider: {provider.get('name')}")
            else:
                print(f"Response: {body[:200]}")
    except Exception as e:
        print(f"Error: {e}")
