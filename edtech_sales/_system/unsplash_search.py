import json, os, sys, urllib.request, urllib.parse
KEY = os.environ["UNSPLASH_ACCESS_KEY"]
slots = json.load(open(sys.argv[1])); out = {}
for slot, q in slots.items():
    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode({"query": q, "per_page": int(os.environ.get("PER_PAGE", 6)), "orientation": "portrait", "content_filter": "high"})
    req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {KEY}", "Accept-Version": "v1"})
    with urllib.request.urlopen(req) as r:
        res = json.load(r); left = r.headers.get("X-Ratelimit-Remaining")
    out[slot] = {"query": q, "results": [{"id": p["id"], "thumb": p["urls"]["small"], "regular": p["urls"]["regular"],
        "desc": p.get("alt_description") or "", "name": p["user"]["name"], "profile": p["user"]["links"]["html"],
        "page": p["links"]["html"], "download_location": p["links"]["download_location"]} for p in res["results"]]}
json.dump(out, open(sys.argv[2], "w"), indent=1); print("rate limit left:", left)
for s, v in out.items(): print(s, len(v["results"]), "|", " / ".join(r["desc"][:50] for r in v["results"][:6]))
