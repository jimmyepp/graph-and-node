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

payloads = [
    # 1. Search for a specific common name
    {"name": "Peter"},
    # 2. Search with typical Kyruus request parameters
    {"searchTerm": "Peter", "page": 1, "pageSize": 10},
    # 3. Simple text query
    {"query": "Peter"},
    # 4. Keyword search
    {"keyword": "Pediatric"},
    # 5. Empty payload to see if it behaves differently
    {}
]

for i, payload in enumerate(payloads, 1):
    data = json.dumps(payload).encode('utf-8')
    print(f"\n--- Testing Payload #{i}: {payload} ---")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
            print(f"Status: {status}")
            print(f"Response Length: {len(body)} bytes")
            try:
                parsed = json.loads(body)
                if "providers" in parsed:
                    print(f"Success! Found {len(parsed['providers'])} providers.")
                    for provider in parsed["providers"][:2]:
                        print(f" - Provider: {provider.get('name')} ({provider.get('specialty')})")
                else:
                    print(f"Response keys: {list(parsed.keys())}")
            except Exception as e:
                print(f"Could not parse JSON. Preview: {body[:300]}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}")
        body = e.read().decode('utf-8', errors='ignore') if e.fp else ""
        print(f"Error body: {body[:200]}")
    except Exception as e:
        print(f"Error: {e}")
