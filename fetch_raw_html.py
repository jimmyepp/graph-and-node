import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.christushealth.org/locations/ross-breast-center"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
        html = response.read().decode('utf-8', errors='ignore')
        with open("/Users/jimmyepperson/Developer/GraphandNode/raw_ross_breast_center.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Raw HTML saved successfully.")
except Exception as e:
    print(f"Error fetching HTML: {e}")
