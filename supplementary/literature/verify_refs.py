"""Verify candidate references against Crossref (title match) and store canonical metadata in references_verified.json."""
import json, re, sys, time, difflib, urllib.parse, urllib.request
H = {"User-Agent": "ref-verifier/0.1"}
def get(u):
    for i in range(5):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60).read())
        except Exception: time.sleep(2 ** i)
def norm(s): return re.sub(r"[^a-z0-9 ]", "", (s or "").lower())
def verify(key, title, author=None, year=None, doi=None):
    if doi:
        m = get("https://api.crossref.org/works/" + urllib.parse.quote(doi)); items = [m["message"]] if m else []
    else:
        p = {"query.bibliographic": title + (" " + author if author else ""), "rows": 5}
        r = get("https://api.crossref.org/works?" + urllib.parse.urlencode(p)); items = r["message"]["items"] if r else []
    best, score = None, 0
    for it in items:
        s = difflib.SequenceMatcher(None, norm(title), norm((it.get("title") or [""])[0])).ratio()
        if s > score: best, score = it, s
    if not best: return dict(key=key, ok=False, query=title)
    au = [f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in best.get("author", [])]
    y = best.get("issued", {}).get("date-parts", [[None]])[0][0]
    return dict(key=key, ok=score > 0.9, score=round(score, 3), doi=best.get("DOI"), title=(best.get("title") or [""])[0],
                authors=au, year=y, venue=(best.get("container-title") or [""])[0], volume=best.get("volume"),
                issue=best.get("issue"), pages=best.get("page") or best.get("article-number"), type=best.get("type"))
if __name__ == "__main__":
    refs = json.load(open(sys.argv[1]))
    try: out = json.load(open("references_verified.json"))
    except Exception: out = {}
    for r in refs:
        v = verify(**r); out[r["key"]] = v
        print(("OK " if v.get("ok") else "?? ") + f"{r['key']:18s} {v.get('score')} | {v.get('year')} | {v.get('doi')} | {(v.get('authors') or [''])[0]} | {v.get('title','')[:90]} | {v.get('venue','')[:40]}")
    json.dump(out, open("references_verified.json", "w"), indent=1)
