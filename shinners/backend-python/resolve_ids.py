import urllib.request

# These are SHORT IDs from the unsplash.com/photos/{id} page
# The download endpoint redirects to the full CDN URL
short_ids = [
    # From fashion search results
    "nimElTcTNyY", "_3Q3tsJ01nc", "BteCp6aq4GI", "TS--uNw-JqE",
    "K0DxxljcRv0", "PKMvkg7vnUo", "OVS3rqXq9gg", "UqT55tGBqzI",
    "dlxLGIy-2VU",
]

full_ids = []
for sid in short_ids:
    url = f"https://unsplash.com/photos/{sid}/download?force=true"
    try:
        req = urllib.request.Request(url, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=8)
        final_url = resp.url
        # Extract the photo-XXXXX part
        if "photo-" in final_url:
            pid = final_url.split("photo-")[1].split("?")[0]
            print(f"  {sid} -> {pid}")
            full_ids.append(pid)
        else:
            print(f"  {sid} -> no photo- in {final_url[:60]}")
    except Exception as e:
        print(f"  {sid} - {str(e)[:50]}")

print(f"\n=== NEW FULL IDs ({len(full_ids)}) ===")
for fid in full_ids:
    print(f'"{fid}",')
