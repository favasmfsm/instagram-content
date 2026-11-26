"""Post carousels to Instagram through the Graph API.

Images are converted to JPEG (Instagram's only supported format) into
public/<account>/<carousel>/, pushed to the public GitHub repo, and handed
to Instagram as raw.githubusercontent.com URLs.

Usage:
  python3 post.py list                         # every carousel and whether it's posted
  python3 post.py next <account>               # dry run: what would post next
  python3 post.py next <account> --live        # actually post it
  python3 post.py next <account> --live --daily  # same, but skip if posted <20h ago
  python3 post.py post <account> <folder>      # dry run for one carousel
  python3 post.py post <account> <folder> --live

Accounts are the keys in accounts.json. Nothing is published without --live.
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_BASE = "https://raw.githubusercontent.com/favasmfsm/instagram-content/main"
POSTED_FILE = ROOT / "posted.json"

# account -> (folder holding the carousels, slide glob, caption file name)
SOURCES = {
    "edtechsalesmaster": (ROOT / "edtech_sales", "png/*.png", "caption.txt"),
    "thesalesfalcon": (ROOT / "sales_falcon" / "carousels", "slide-*.png", "caption.md"),
}


# ---------- carousels ----------

def carousels(account):
    base, glob, cap = SOURCES[account]
    out = []
    for d in sorted(base.iterdir()):
        if not d.is_dir() or not d.name[:1].isdigit():
            continue
        slides = sorted(d.glob(glob))
        if slides and (d / cap).exists():
            out.append({"folder": d.name, "dir": d, "slides": slides,
                        "caption": (d / cap).read_text().strip()})
    return out


def find(account, folder):
    for c in carousels(account):
        if c["folder"] == folder:
            return c
    sys.exit(f"No carousel '{folder}' for {account}. Run: python3 post.py list")


def problems(c):
    p = []
    if not 2 <= len(c["slides"]) <= 10:
        p.append(f"{len(c['slides'])} slides (Instagram needs 2-10)")
    if len(c["caption"]) > 2200:
        p.append(f"caption is {len(c['caption'])} characters (max 2200)")
    tags = c["caption"].count("#")
    if tags > 30:
        p.append(f"{tags} hashtags (max 30)")
    return p


def load_posted():
    return json.loads(POSTED_FILE.read_text()) if POSTED_FILE.exists() else {}


# ---------- images ----------

def to_jpegs(account, c):
    out_dir = ROOT / "public" / account / c["folder"]
    out_dir.mkdir(parents=True, exist_ok=True)
    jpgs = []
    for i, png in enumerate(c["slides"], 1):
        jpg = out_dir / f"{i:02d}.jpg"
        if not jpg.exists():
            try:
                from PIL import Image
                Image.open(png).convert("RGB").save(jpg, "JPEG", quality=92)
            except ImportError:  # macOS without Pillow
                subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92",
                                str(png), "--out", str(jpg)], check=True, capture_output=True)
        jpgs.append(jpg)
    return jpgs


def git_push(paths, message):
    rel = [str(p.relative_to(ROOT)) for p in paths]
    subprocess.run(["git", "add", "--", *rel], cwd=ROOT, check=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", *rel], cwd=ROOT)
    if staged.returncode != 0:
        subprocess.run(["git", "commit", "-q", "-m", message, "--", *rel], cwd=ROOT, check=True)
    subprocess.run(["git", "pull", "-q", "--rebase", "--autostash"], cwd=ROOT, check=True)
    subprocess.run(["git", "push", "-q"], cwd=ROOT, check=True)


def load_accounts():
    # On GitHub Actions the file comes from the ACCOUNTS_JSON secret.
    env = os.environ.get("ACCOUNTS_JSON")
    return json.loads(env) if env else json.loads((ROOT / "accounts.json").read_text())


def hours_since_last_post(account):
    times = [datetime.strptime(v["at"], "%Y-%m-%dT%H:%M:%S%z")
             for v in load_posted().get(account, {}).values()]
    if not times:
        return None
    return (datetime.now(timezone.utc) - max(times)).total_seconds() / 3600


def url_for(path):
    return f"{RAW_BASE}/{urllib.parse.quote(str(path.relative_to(ROOT)))}"


def wait_public(urls, timeout=120):
    deadline = time.time() + timeout
    for u in urls:
        while True:
            try:
                with urllib.request.urlopen(urllib.request.Request(u, method="HEAD")) as r:
                    if r.status == 200:
                        break
            except urllib.error.HTTPError:
                pass
            if time.time() > deadline:
                sys.exit(f"Image never became public: {u}")
            time.sleep(3)


# ---------- Graph API ----------

def api_base(token):
    host = "graph.instagram.com" if token.startswith("IG") else "graph.facebook.com"
    return f"https://{host}/v27.0"


class APIError(Exception):
    pass


# Graph API throttling codes: 4 = app limit, 17 = user limit, 32 = page limit, 613 = rate limit.
RATE_LIMIT_CODES = {4, 17, 32, 613}
RATE_LIMIT_WAITS = [60, 120, 240]  # seconds between retries when throttled


def call(token, method, path, retry=True, **params):
    params["access_token"] = token
    data = urllib.parse.urlencode(params).encode()
    url = f"{api_base(token)}/{path}"
    waits = list(RATE_LIMIT_WAITS) if retry else []
    while True:
        if method == "GET":
            req = urllib.request.Request(f"{url}?{data.decode()}")
        else:
            req = urllib.request.Request(url, data=data, method="POST")
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            err = json.loads(e.read() or b"{}").get("error", {})
            msg = f"Instagram API error on {path}: {err.get('message', e)}"
            if err.get("code") in RATE_LIMIT_CODES and waits:
                w = waits.pop(0)
                print(f"  {msg} - waiting {w}s and retrying")
                time.sleep(w)
                continue
            raise APIError(msg)


def wait_ready(token, container_id, timeout=300):
    # Poll gently: every status check counts against the app's hourly call limit.
    deadline = time.time() + timeout
    delay = 3
    while time.time() < deadline:
        time.sleep(delay)
        status = call(token, "GET", container_id, fields="status_code").get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            raise APIError(f"Container {container_id} failed with status {status}")
        delay = min(delay * 2, 30)
    raise APIError(f"Container {container_id} not ready after {timeout}s")


def find_published(token, ig_id, caption, since):
    """Return the post with this caption published at/after `since`, if Instagram made it live."""
    data = call(token, "GET", f"{ig_id}/media", fields="id,permalink,timestamp,caption", limit=5)
    for m in data.get("data", []):
        at = datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        if at >= since and (m.get("caption") or "").strip() == caption.strip():
            return m
    return None


def quota(token, ig_id):
    data = call(token, "GET", f"{ig_id}/content_publishing_limit", fields="quota_usage,config")
    row = (data.get("data") or [{}])[0]
    return row.get("quota_usage"), (row.get("config") or {}).get("quota_total")


# ---------- commands ----------

def cmd_list():
    posted = load_posted()
    for account in SOURCES:
        print(f"\n{account}")
        for c in carousels(account):
            done = posted.get(account, {}).get(c["folder"])
            mark = f"posted {done['at'][:10]}" if done else "-"
            warn = "; ".join(problems(c))
            print(f"  {c['folder']:<32} {len(c['slides']):>2} slides  {mark}"
                  + (f"  !! {warn}" if warn else ""))


def cmd_post(account, folder, live):
    accounts = load_accounts()
    if account not in accounts or account not in SOURCES:
        sys.exit(f"Unknown account '{account}'. Choose from: {', '.join(SOURCES)}")
    token, ig_id = accounts[account]["token"], accounts[account]["ig_id"]
    c = find(account, folder)
    posted = load_posted()

    print(f"{account} <- {c['folder']}  ({len(c['slides'])} slides, {len(c['caption'])} caption chars)")
    if c["folder"] in posted.get(account, {}):
        sys.exit("Already posted. Remove it from posted.json to post again.")
    bad = problems(c)
    if bad:
        sys.exit("Can't post: " + "; ".join(bad))
    used, total = quota(token, ig_id)
    print(f"Publishing quota: {used}/{total} used in the last 24h")
    if used is not None and total is not None and used >= total:
        sys.exit("Daily publishing limit reached; try again later.")

    if not live:
        print("\nCaption preview:\n" + "\n".join("  | " + l for l in c["caption"].splitlines()[:6]))
        print("\nDry run only. Add --live to convert, push the images and publish.")
        return

    jpgs = to_jpegs(account, c)
    print(f"Pushing {len(jpgs)} JPEGs to GitHub...")
    git_push(jpgs, f"Add images for {account}/{c['folder']}")
    urls = [url_for(j) for j in jpgs]
    wait_public(urls)

    print("Uploading slides to Instagram...")
    children = []
    for u in urls:
        cid = call(token, "POST", f"{ig_id}/media", image_url=u, is_carousel_item="true")["id"]
        wait_ready(token, cid)
        children.append(cid)
    carousel = call(token, "POST", f"{ig_id}/media", media_type="CAROUSEL",
                    children=",".join(children), caption=c["caption"])["id"]
    wait_ready(token, carousel)

    # media_publish must not be blindly retried: Instagram sometimes publishes the post
    # and still returns an error, so a retry would post it twice. Check first.
    started = datetime.now(timezone.utc).replace(microsecond=0)
    try:
        media_id = call(token, "POST", f"{ig_id}/media_publish", retry=False,
                        creation_id=carousel)["id"]
        link = call(token, "GET", media_id, fields="permalink").get("permalink")
        at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
    except APIError as e:
        print(f"  {e} - checking whether it went live anyway...")
        m = None
        for w in [30] + RATE_LIMIT_WAITS:
            time.sleep(w)
            try:
                m = find_published(token, ig_id, c["caption"], started.replace(second=0))
                if m:
                    break
                status = call(token, "GET", carousel, fields="status_code").get("status_code")
            except APIError as e2:
                print(f"  {e2}")
                continue
            if status == "FINISHED":  # still unpublished and publishable: try once more
                print("  Not live yet; publishing again...")
                try:
                    media_id = call(token, "POST", f"{ig_id}/media_publish", retry=False,
                                    creation_id=carousel)["id"]
                    m = {"id": media_id,
                         "permalink": call(token, "GET", media_id, fields="permalink").get("permalink"),
                         "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")}
                    break
                except APIError as e3:
                    print(f"  {e3}")
        if not m:
            raise APIError(f"Publish failed and the post is not live: {e}")
        media_id, link, at = m["id"], m["permalink"], m["timestamp"]
    print(f"Published: {link}")

    posted.setdefault(account, {})[c["folder"]] = {
        "media_id": media_id, "permalink": link, "at": at,
    }
    POSTED_FILE.write_text(json.dumps(posted, indent=2, ensure_ascii=False) + "\n")
    changed = [POSTED_FILE] + mark_csv_posted(account, c["folder"])
    git_push(changed, f"Posted {account}/{c['folder']}")


def mark_csv_posted(account, folder):
    """Set Status=Posted for this carousel in the account's ideas CSV, if it has one."""
    import csv, io
    path = SOURCES[account][0] / "carousel-ideas.csv"
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:  # keep CRLF line endings
        raw = f.read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    rows = list(csv.reader(io.StringIO(raw)))
    head = rows[0]
    if "Folder" not in head or "Status" not in head:
        return []
    fi, si = head.index("Folder"), head.index("Status")
    for r in rows[1:]:
        if len(r) > fi and r[fi] == folder:
            r[si] = "Posted"
    buf = io.StringIO()
    csv.writer(buf, lineterminator=nl).writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8-sig")
    return [path]


def cmd_next(account, live, daily=False):
    if account not in SOURCES:
        sys.exit(f"Unknown account '{account}'. Choose from: {', '.join(SOURCES)}")
    if daily:
        h = hours_since_last_post(account)
        if h is not None and h < 20:
            print(f"{account}: last post was {h:.1f}h ago; skipping today.")
            return
    done = load_posted().get(account, {})
    for c in carousels(account):
        if c["folder"] not in done:
            return cmd_post(account, c["folder"], live)
    print(f"Everything for {account} is posted.")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    live = "--live" in sys.argv
    try:
        if args[:1] == ["list"]:
            cmd_list()
        elif args[:1] == ["next"] and len(args) == 2:
            cmd_next(args[1], live, daily="--daily" in sys.argv)
        elif args[:1] == ["post"] and len(args) == 3:
            cmd_post(args[1], args[2], live)
        else:
            print(__doc__)
    except APIError as e:
        sys.exit(str(e))
