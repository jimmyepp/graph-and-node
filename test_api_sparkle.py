import urllib.request
import urllib.error
import json
import ssl
import re

# Ignore SSL certificate verification if needed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base_url = "https://www.christushealth.org"

endpoints = {
    "allTaxons": "/api/doctorlocations/Taxonomy",
    "appointments": "/api/doctorlocations/getprovidersappointmentdata",
    "locations": "/api/doctorlocations/Locations",
    "pageTaxons": "/api/doctorlocations/CurrentPageServicesTaxons",
    "providers": "/api/doctorlocations/GetProviderData",
    "services": "/api/doctorlocations/services",
    "synonyms": "/api/doctorlocations/Synonyms",
    "specialties": "/api/doctorlocations/Specialties",
    "news": "/api/newsandevents/news",
    "provideridsforkeywords": "/api/sitecore/kyruus/ProviderIdsForKeywords",
    "kyruusSearch": "/api/sitecore/kyruus/search",
    "providerSettings": "/api/doctorlocations/GetProviderSettingsData"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*"
}

results = {}

for name, endpoint in endpoints.items():
    url = base_url + endpoint
    results[name] = {"get": {"success": False}, "post": {"success": False}}
    
    # Test GET
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            body = response.read().decode('utf-8', errors='ignore')
            results[name]["get"] = {
                "success": True,
                "status": response.status,
                "length": len(body),
                "sparkle_count": len(re.findall(r"sparkle", body, re.IGNORECASE)),
                "sparkle_samples": [body[max(0, m.start()-50):min(len(body), m.end()+100)] for m in re.finditer(r"sparkle", body, re.IGNORECASE)][:5]
            }
    except urllib.error.HTTPError as e:
        results[name]["get"] = {
            "success": False,
            "error": f"HTTP {e.code}"
        }
    except Exception as e:
        results[name]["get"] = {
            "success": False,
            "error": str(e)
        }

    # Test POST
    req_post = urllib.request.Request(url, data=b"{}", headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req_post, context=ctx, timeout=15) as response:
            body = response.read().decode('utf-8', errors='ignore')
            results[name]["post"] = {
                "success": True,
                "status": response.status,
                "length": len(body),
                "sparkle_count": len(re.findall(r"sparkle", body, re.IGNORECASE)),
                "sparkle_samples": [body[max(0, m.start()-50):min(len(body), m.end()+100)] for m in re.finditer(r"sparkle", body, re.IGNORECASE)][:5]
            }
    except urllib.error.HTTPError as e:
        results[name]["post"] = {
            "success": False,
            "error": f"HTTP {e.code}"
        }
    except Exception as e:
        results[name]["post"] = {
            "success": False,
            "error": str(e)
        }

# Output report in a clean format
print("\n=== API EXECUTION & SPARKLE REPORT ===")
print(json.dumps(results, indent=2))
