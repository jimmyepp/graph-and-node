import urllib.request
import urllib.error
import json
import ssl

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

print("Starting API test on christushealth.org...")
for name, endpoint in endpoints.items():
    url = base_url + endpoint
    print(f"\nTesting {name} ({url})...")
    
    # Try GET first
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
            print(f"  GET Response Status: {status}")
            preview = body[:300]
            print(f"  GET Content Preview: {preview}")
            
            # Check for sparkle
            if "sparkle" in body.lower():
                print(f"  *** SPARKLE FOUND in GET response! ***")
                # print matches
                idx = body.lower().find("sparkle")
                print(f"  Match snippet: {body[max(0, idx-50):min(len(body), idx+100)]}")
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode('utf-8', errors='ignore') if e.fp else ""
        print(f"  GET Failed (HTTP {status})")
        if body:
            print(f"  GET Error body (preview): {body[:200]}")
            if "sparkle" in body.lower():
                print(f"  *** SPARKLE FOUND in GET Error response! ***")
    except Exception as e:
        print(f"  GET Error: {e}")

    # Also try a mock POST (empty JSON) just in case it requires POST
    req_post = urllib.request.Request(url, data=b"{}", headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req_post, context=ctx, timeout=10) as response:
            status = response.status
            body = response.read().decode('utf-8', errors='ignore')
            print(f"  POST Response Status: {status}")
            preview = body[:300]
            print(f"  POST Content Preview: {preview}")
            
            # Check for sparkle
            if "sparkle" in body.lower():
                print(f"  *** SPARKLE FOUND in POST response! ***")
                idx = body.lower().find("sparkle")
                print(f"  Match snippet: {body[max(0, idx-50):min(len(body), idx+100)]}")
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode('utf-8', errors='ignore') if e.fp else ""
        if status != 405: # ignore method not allowed
            print(f"  POST Failed (HTTP {status})")
            if body:
                print(f"  POST Error body (preview): {body[:200]}")
                if "sparkle" in body.lower():
                    print(f"  *** SPARKLE FOUND in POST Error response! ***")
    except Exception as e:
        pass
