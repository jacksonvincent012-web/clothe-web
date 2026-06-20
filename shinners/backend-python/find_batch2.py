import urllib.request

# IDs found in web searches - most are from Unsplash fashion/photo pages
ids = [
    # From fashion product search page
    "dwKiHoqqxk8", "KStSiM1UvPw", "E-0ON3VGrBc", "S4h-v_bcQwo",
    "e8sbQNYEwX8", "ME4hmIGXPHA", "2ANGZ3ZFerY", "E4o2jhHdrvw",
    "DIRCSVQguVw", "onVboUyFuHI", "0jjksk2_W78", "3DNS-ibDu0U",
    "iAWeqRrfYIA", "48Nu3kMxd4A", "TXD_Oj2B2V0",
    # From Unsplash developer docs
    "LBI7cgq3pbM", "eOLpJytrbsQ", "Dwu85P9SOIk", "pFqrYbhIAXs",
    "mtNweauBsMQ", "cu28RXNesPo", "1523476843875-43c2cb89aa85",
    # From fashion flat lay
    "DMUFAvIh6aE",
    # From dev article
    "1725610588086-b9e38da987f7",
    # From 1440 search
    "1OqcFvef3YA", "2fMnBF42EzE", "WNdN495Ub0w", "dw2zLK4edqQ",
    "YtJ5u4ATRYc", "t4FKTUdmxwc", "-OezGl_E7Xs", "q6ztmn9uaxE",
    "418RL_VHZuE", "HX7zpOs2ePM", "IMtfsr5vCAs", "7QwpHLcp45U",
    "zZ7JENPrxc0", "-tFyUdIOcio", "TkmJIHRnkY4",
]

working = []
for i, pid in enumerate(ids):
    url = f"https://images.unsplash.com/photo-{pid}?w=100&q=60"
    try:
        req = urllib.request.Request(url, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=5)
        print(f"  OK: {pid[:20]} ({resp.status})")
        working.append(pid)
    except Exception as e:
        code = str(e)[-30:] if hasattr(e, 'code') else str(e)[:40]
        print(f"  FAIL: {pid[:20]} - {code}")

print(f"\n=== WORKING IDs ({len(working)}) ===")
for w in working:
    print(f'"{w}",')
