import json, os, sys, urllib.request
KEY = os.environ["UNSPLASH_ACCESS_KEY"]
H = {"Authorization": f"Client-ID {KEY}", "Accept-Version": "v1"}
picks = json.load(open(sys.argv[1]))  # {carousel: {slot: [searchfile, searchkey, index]}}
for car, slots in picks.items():
    os.makedirs(f"{car}/photos", exist_ok=True)
    meta = json.load(open(f"{car}/photos.json")) if os.path.exists(f"{car}/photos.json") else {}
    for slot, (sf, key, idx) in slots.items():
        r = json.load(open(sf))[key]["results"][idx - 1]
        # register the download with Unsplash (API guideline)
        urllib.request.urlopen(urllib.request.Request(r["download_location"], headers=H)).read()
        fn = f"photos/{slot}-{r['id']}.jpg"
        req = urllib.request.Request(r["regular"].replace("w=1080", "w=1400"), headers={"User-Agent": "carousel-builder"})
        open(f"{car}/{fn}", "wb").write(urllib.request.urlopen(req).read())
        meta[slot] = {"file": fn, "name": r["name"], "profile": r["profile"], "page": r["page"], "id": r["id"]}
        print(car, slot, r["name"], os.path.getsize(f"{car}/{fn}") // 1024, "KB")
    json.dump(meta, open(f"{car}/photos.json", "w"), indent=1)
