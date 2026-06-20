import urllib.request

# More IDs from developer docs and searching
ids = [
    "1417325384643-aac51acc9e5d",  # from Unsplash API docs
    "1479862863327-e4d9a0a83c3d",  # from Unsplash API docs
    "1523476843875-43c2cb89aa85",  # already known
    "1725610588086-b9e38da987f7",  # from dev article - new!
]

working = []
for pid in ids:
    url = f"https://images.unsplash.com/photo-{pid}?w=100&q=60"
    try:
        req = urllib.request.Request(url, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=5)
        print(f"  OK: {pid} ({resp.status})")
        working.append(pid)
    except Exception as e:
        code = str(e)[:50] if hasattr(e, 'code') else str(e)[:50]
        print(f"  FAIL: {pid} - {code}")

print(f"\n=== WORKING: {len(working)} ===")
for w in working:
    print(f'"{w}",')
