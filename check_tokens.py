"""Check that each token in accounts.json works for its Instagram account.

Usage: python3 check_tokens.py
"""
import json
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

def api_for(token):
    # Instagram Login tokens (IGAA...) use graph.instagram.com;
    # Facebook Login / system user tokens (EAA...) use graph.facebook.com.
    host = "graph.instagram.com" if token.startswith("IG") else "graph.facebook.com"
    return f"https://{host}/v27.0"


accounts = json.loads((Path(__file__).parent / "accounts.json").read_text())

for name, acc in accounts.items():
    token = acc.get("token", "")
    if not token or token == "PASTE_TOKEN_HERE":
        print(f"[skip] {name}: no token yet")
        continue
    qs = urllib.parse.urlencode({"fields": "id,username", "access_token": token})
    try:
        with urllib.request.urlopen(f"{api_for(token)}/{acc['ig_id']}?{qs}") as r:
            data = json.load(r)
        ok = data.get("id") == acc["ig_id"]
        print(f"[{'ok' if ok else 'mismatch'}] {name}: @{data.get('username')} (id {data.get('id')})")
    except urllib.error.HTTPError as e:
        err = json.loads(e.read() or b"{}").get("error", {})
        print(f"[error] {name}: {err.get('message', e)}")
