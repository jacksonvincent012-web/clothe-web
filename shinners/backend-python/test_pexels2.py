import urllib.request

pexels_ids = [11844304, 6833756, 7081105, 5325695, 7969812, 833169]

for pid in pexels_ids:
    url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg"
    req = urllib.request.Request(url, method="HEAD")
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        print(f"  OK: {pid} ({resp.status})")
        # Check content-type
        ct = resp.headers.get("Content-Type", "unknown")
        print(f"      Type: {ct}")
    except Exception as e:
        print(f"  FAIL: {pid} - {str(e)[:60]}")
