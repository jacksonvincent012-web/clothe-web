import urllib.request, re

# MORE short IDs extracted from various search results
more_short_ids = [
    # From fashion search pages (more results visible)
    "xXJ6utyoSw0", "GLg0z5z8EQU", "GbveIG8YKMk", "mwa_nzFpnJw",
    "4Hmj9gkyM6c",
    # From clothing page
    "n6B49lHZx4U", "EI1Gk9rWZ_I", "tSZ2B3r0yJc", "v_0UllFLN4Y",
    "ZALH8QdIMgY", "Lr1mRgSd5_M", "H-pXUMv6hsc",
    # Generic fashion
    "pFqrYbhIAXs", "mtNweauBsMQ", "Dwu85P9SOIk",
    # More from search
    "Mgcewi66j7M", "JR1QGR2phV4", "f4RlRqg-H4g", "ogLKlWRpXr4",
    "it4JAfmSWIQ", "Pj2C2tMlGXg", "Z22Uiu5MhV4",
]

full_ids = []
for sid in more_short_ids:
    url = f"https://unsplash.com/photos/{sid}/download?force=true"
    try:
        req = urllib.request.Request(url, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=8)
        final_url = resp.url
        if "photo-" in final_url:
            pid = final_url.split("photo-")[1].split("?")[0]
            print(f"  {sid[:15]:15s} -> {pid}")
            full_ids.append(pid)
        else:
            print(f"  {sid[:15]:15s} -> no match: {final_url[:50]}")
    except Exception as e:
        print(f"  {sid[:15]:15s} -> {str(e)[:40]}")

print(f"\n=== NEW FULL IDs ({len(full_ids)}) ===")
for fid in full_ids:
    print(f'"{fid}",')
