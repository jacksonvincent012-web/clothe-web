import urllib.request

# Pexels IDs found in search results (fashion/clothing photos)
pexels_ids = [
    11844304, 6833756, 7081105, 5325695, 6153353, 5560194,
    7969812, 5325774, 5325639, 6153355, 5560195, 7081104,
    6153374, 6069964, 19909750, 833169, 5236997,
    29538558, 8018040, 10203170, 8126621, 12655540,
    30512491, 4510111, 15327091, 15927094,
    31839879, 977909, 1377451, 6181979, 27863598,
    28517485, 1000373, 2307879, 3507016, 7758138,
    9701509, 35391601, 27532793, 28988331, 1377454,
    14995950, 6181955, 6181981, 12585895, 10622546,
    7081107, 5325771, 30816952, 31773617, 21390399,
    5560606, 5325696, 15160206, 9821877, 19198606,
    5325768, 35984078
]

working = []
for pid in pexels_ids:
    url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=100&h=125&fit=crop"
    try:
        req = urllib.request.Request(url, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=5)
        print(f"  OK: {pid}")
        working.append(pid)
    except Exception as e:
        # Try with .png extension
        url2 = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.png?auto=compress&cs=tinysrgb&w=100&h=125&fit=crop"
        try:
            req = urllib.request.Request(url2, method="HEAD")
            resp = urllib.request.urlopen(req, timeout=5)
            print(f"  OK: {pid} (png)")
            working.append(pid)
        except:
            print(f"  FAIL: {pid}")

print(f"\n=== WORKING PEXELS IDs ({len(working)}) ===")
for w in working:
    print(f"{w},")
